import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from pymongo import errors as pymongo_errors
from django.db import transaction
import datetime 
from bson import ObjectId

from Utils.db import connect_to_mongo, connect_to_gridfs
from Utils.helper_functions import get_file_id_by_name, get_general_info_metadata, get_nlp_analysis_metadata, get_text_from_pdf
from api.serializers import DocGeneralInfoSerializer, NlpAnalysisSerializer
from Utils.decorators import timing_decorator
from Nlp.wordcloud_generator_testing import test_word_cloud
from Nlp.categorization import predict_label_from_string
from Nlp.name_entity_recognition import extract_information
from Nlp.nlp_analysis import extract_metadata_pdf
from api.models import CategoryDocumentCount
from Nlp.nlp_analysis_optimized import extract_metadata, summarize_pdf

import chromadb
import tempfile
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.cohere import Cohere
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import SummaryIndex
from llama_index.embeddings.cohere.base import CohereEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext, load_index_from_storage
from WebScraping.initializations import parser, index



@timing_decorator
@api_view(['POST'])
def add_pdf(request):
    try:
        pdf_file = request.FILES.get('file')
        print(pdf_file)
        if not pdf_file:
            return Response({'error': 'No PDF file provided'}, status=400)
        
        if not pdf_file.name.endswith('.pdf'):
            return Response({'error': 'Invalid file type'}, status=400)
        fs = connect_to_gridfs()
        db = connect_to_mongo()
        
        existing_file = fs.find_one({'filename': pdf_file.name })
        if existing_file:
            return Response({'error': 'File already exists'}, status=400)
        
        file_id = fs.put(pdf_file, filename=pdf_file.name)
        title = pdf_file.name
        metadata_dict1 = extract_metadata_pdf(pdf_file)
        metadata_dict = extract_metadata(pdf_file)
        print(metadata_dict["title"])
        if metadata_dict['title'] != "No title found":
            title = metadata_dict["title"]
            existing_file = fs.find_one({'filename': title})
            if existing_file:
                fs.delete(file_id)
                return Response({'error': 'File already exists'}, status=400)
        
        db.fs.files.update_one({'_id': file_id}, {'$set': {'filename': title}})
        with transaction.atomic():
            general_info_data = {
                'source': 'PDF',
                'title': title,
                'author': metadata_dict['author']
            }
            general_info_serializer = DocGeneralInfoSerializer(data=general_info_data)
            if general_info_serializer.is_valid():
                general_info = general_info_serializer.save()
                
            else:
                return Response({'error': 'Failed to add DocGeneralInfo', 'details': general_info_serializer.errors}, status=400)
            
            content = get_text_from_pdf(file_id)

            filename = f"{title}.txt"
            filtered_filename = filename.replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ")

            with open(filtered_filename,"w",encoding="utf-8") as temp_file:
                temp_file.write(content)

            file_extractor = {".txt": parser}

            documents = SimpleDirectoryReader(input_files=[filtered_filename],
                                                file_extractor = file_extractor).load_data()
            print("document sent to llamaparse")
            directory = os.getcwd()
            os.remove(f"{directory}/{filtered_filename}")
            print("Document temp file deleted")
            index.insert(documents[0])
            print("document inserted to index!")

            category = "Other"
            ner = {}
            if content != "":
                category = predict_label_from_string(content)
                ner = extract_information(content)
            
            nlp_analysis_data = {
                'nlp_id': general_info.nlp_id,
                'document_type': 'PDF',
                'summary': summarize_pdf(pdf_file),  # Add your summarization logic here
                'category': category,  # Example category, change as needed
                'language': "en",  # Example language, change as needed  metadata_dict1["language"]
                'ner': ner,  
                'confidentiality_level': metadata_dict1["confidentiality"],  # Example confidentiality level, change as needed
                'location': metadata_dict1["locations"],  # Example location, change as needed
                'references': metadata_dict1["references"],
                'in_text_citations': metadata_dict1["in_text_citations"],  # Example uploader, change as needed
                'word_count': metadata_dict1["word_count"]
            }
            nlp_analysis_serializer = NlpAnalysisSerializer(data=nlp_analysis_data)
            if nlp_analysis_serializer.is_valid():
                nlp_analysis_serializer.save()
                #test_word_cloud(content)
            else:
                
                return Response({'error': 'Failed to add NlpAnalysis', 'details': nlp_analysis_serializer.errors}, status=400)
        
        return Response({'message': 'PDF, metadata, and NLP_analysis added successfully', 'file_id': str(file_id)})
        
    except pymongo_errors.PyMongoError as e:
        return Response({'error': str(e)}, status=400)

@timing_decorator 
@api_view(['GET'])
def get_pdf_by_id(request, file_id):
    try:
        if not ObjectId.is_valid(file_id):
            return HttpResponse('Invalid file ID', status=400)
        fs = connect_to_gridfs()
        
        file = fs.get(ObjectId(file_id))  # Corrected "Objectid" to "ObjectId"
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except pymongo_errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)

@timing_decorator
@api_view(['GET'])
def get_pdf_by_name(request, file_name):
    file_id = get_file_id_by_name(file_name)
    print("ahlennnn ana honnn \n\n", file_id)
    if file_id:
        return redirect('get_pdf_by_id', file_id=file_id)
    else:
        return HttpResponse('File not found', status=404)

@timing_decorator
@api_view(['GET', 'POST'])
def list_pdfs(request):
    try:
        db = connect_to_mongo()
        files_collection = db['general_info']
        files = files_collection.find({}, {'title': 1, 'source': 1})  # Include 'source' in the projection
        file_list = [{'name': file['title']} for file in files if file['source'] == "PDF"]
        return JsonResponse({'files': file_list})
    except pymongo_errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)   

@timing_decorator     
@api_view(['POST'])
def handle_selected_pdfs(request):
    try:
        data = request.data
        if data is None:
            return Response({'error': 'Request data is missing'}, status=400)
        selected_pdfs = data.get('selectedPdfs', [])
        if len(selected_pdfs) == 0:
            return Response({'message': 'No PDFs selected'}, status=200)
        
        pdf_file_ids = []
        for pdf_name in selected_pdfs:
            print(pdf_name)
            file_id = get_file_id_by_name(pdf_name)
            if file_id:
                pdf_file_ids.append(file_id)
            else:
                return Response({'error': f'File not found: {pdf_name}'}, status=404)

        pdf_urls = [request.build_absolute_uri(reverse('get_pdf_by_id', args=[file_id])) for file_id in pdf_file_ids]
        print(pdf_urls)
        
        return Response({'message': 'PDFs found', 'pdfUrls': pdf_urls})  # Corrected this line by adding the missing parenthesis
    except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

@timing_decorator
@api_view(['POST'])
def get_metadata_by_pdf_name(request):
    try:
        data = request.data
        print("Request data:", data)
        selected_pdfs = data.get('selectedPdfs', [])

        if len(selected_pdfs) == 0:
            return Response({'message': 'No PDFs selected'}, status=200)

        metadata_list = []
        for pdf_name in selected_pdfs:
            print(f"Processing PDF: {pdf_name}")
            general_info_metadata = get_general_info_metadata(pdf_name)
            nlp_analysis_metadata = get_nlp_analysis_metadata(pdf_name)
            
            if not general_info_metadata:
                print(f"No general info metadata found for: {pdf_name}")
            if not nlp_analysis_metadata:
                print(f"No NLP analysis metadata found for: {pdf_name}")

            for gen_info, nlp_info in zip(general_info_metadata, nlp_analysis_metadata):
                combined_metadata = {
                    'general_info': gen_info,
                    'nlp_analysis': nlp_info
                }
                metadata_list.append(combined_metadata)
        logging.info(f"Combined Metadata: {metadata_list}")
        return Response({'message': 'PDFs found', 'pdf_metadata': metadata_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    


@timing_decorator
@api_view(['GET'])
def get_all_metadata(request):
    try:
        db = connect_to_mongo()
        general_info_collection = db['general_info']
        nlp_analysis_collection = db['nlp_analysis']
        
        general_info_docs = list(general_info_collection.find())
        nlp_analysis_docs = list(nlp_analysis_collection.find())
        combined_data = {}

        # Process general_info documents
        for doc in general_info_docs:
            nlp_id = doc.get('nlp_id')
            if nlp_id:
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                combined_data[nlp_id] = combined_data.get(nlp_id, {})
                combined_data[nlp_id].update(doc)

        # Process nlp_analysis documents
        for doc in nlp_analysis_docs:
            nlp_id = doc.get('nlp_id')
            if nlp_id:
                if isinstance(nlp_id, dict) and '$numberLong' in nlp_id:
                    nlp_id = int(nlp_id['$numberLong'])
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
                combined_data[nlp_id] = combined_data.get(nlp_id, {})
                combined_data[nlp_id].update(doc)

        # Convert combined data to a list
        combined_data_list = list(combined_data.values())

        return JsonResponse(combined_data_list, safe=False)
    except pymongo_errors.PyMongoError as e:
        return HttpResponse(f'Database error: {str(e)}', status=500)
    


@timing_decorator
@api_view(['GET'])
def category_document_count(request):
    data = list(CategoryDocumentCount.objects.values('category', 'document_count'))
    return JsonResponse(data, safe=False)
