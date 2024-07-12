# from initializations.initializer import cohere_api_key
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# import cohere
# from Utils.decorators import timing_decorator
# from fpdf import FPDF
# import os
# import logging
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import redirect
# from django.urls import reverse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from bson.objectid import ObjectId
# from pymongo import errors as pymongo_errors
# from django.db import transaction
# import datetime 
# from bson import ObjectId

# from Utils.db import connect_to_mongo, connect_to_gridfs

# co = cohere.Client(api_key=cohere_api_key)

# preamble = """you are a legal llm,  made to assist the client in their legal tasks.
# Your main task will be to generate sample documents based off their request.
# do not respond with anything other than the document sample.
# do not respond with anything other than what the client asked for.
# avoid giving any remarks to client or writing anything other than he asks.
# respond in english.
# The response will be written into a pdf, do not format in .md"""

# @timing_decorator
# @api_view(['POST'])
# def generate_document(request):

#     global chat_history
#     query = request.data.get('query')
#     file_name = request.data.get('file_name')

#     if not query:
#         return Response({'error': 'No query provided'}, status=400)
    
#     stream = co.chat_stream(
#         model='command-r-plus',
#         preamble=preamble,  
#         message=f'{preamble} <Query: {query}>',
#         temperature=0.5,
#         prompt_truncation='AUTO',
#         connectors=[{"id": "web-search"}]
#     )

#     response_text = ""
#     for event in stream:
#         if event.event_type == "text-generation":
#             response_text += event.text

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     textfile_name = f"{file_name}.txt"
#     with open(textfile_name, "w", encoding='utf-8') as file:
#         file.write(response_text)

#     with open(textfile_name, "r", encoding='utf-8') as file:
#         for line in file:
#             if pdf.get_y() > 260:  # Check if we are at the bottom of the page
#                 pdf.add_page()
#             pdf.multi_cell(0, 10, txt=line, align='L')

#     directory = os.getcwd()
#     os.remove(f"{directory}/{textfile_name}")

#     pdf.output(f"{file_name}.pdf")



#     return Response({'response': response_text}, status=200)

################Trying################

import os
import logging
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fpdf import FPDF
import cohere
from initializations.initializer import cohere_api_key
from Utils.decorators import timing_decorator
from Utils.db import connect_to_mongo, connect_to_gridfs

# Initialize cohere client
co = cohere.Client(api_key=cohere_api_key)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define preamble
preamble = """you are a legal llm, made to assist the client in their legal tasks.
Your main task will be to generate sample documents based off their request.
do not respond with anything other than the document sample.
do not respond with anything other than what the client asked for.
avoid giving any remarks to client or writing anything other than he asks.
respond in english.
The response will be written into a pdf, do not format in .md"""

@timing_decorator
@api_view(['POST'])
def generate_document(request):
    query = request.data.get('query')
    file_name = request.data.get('file_name')

    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
    try:
        response_text = generate_response(query)
        pdf_path = create_pdf(response_text, file_name)
        file_id, title = save_to_gridfs(file_name, pdf_path)
        return Response({'response': response_text, 'file_id': str(file_id)}, status=200)
    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return Response({'error': 'Failed to generate document'}, status=500)

def generate_response(query):
    """Generates a response from the cohere API."""
    stream = co.chat_stream(
        model='command-r-plus',
        preamble=preamble,  
        message=f'{preamble} <Query: {query}>',
        temperature=0.5,
        prompt_truncation='AUTO',
        connectors=[{"id": "web-search"}]
    )

    response_text = ""
    for event in stream:
        if event.event_type == "text-generation":
            response_text += event.text

    return response_text

def create_pdf(response_text, file_name):
    """Creates a PDF from the given text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    textfile_name = f"{file_name}.txt"
    try:
        with open(textfile_name, "w", encoding='utf-8') as file:
            file.write(response_text)

        with open(textfile_name, "r", encoding='utf-8') as file:
            for line in file:
                if pdf.get_y() > 260:  # Check if we are at the bottom of the page
                    pdf.add_page()
                pdf.multi_cell(0, 10, txt=line, align='L')

        directory = os.getcwd()
        os.remove(f"{directory}/{textfile_name}")

        pdf_path = f"{file_name}.pdf"
        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        raise

def save_to_gridfs(file_name, file_path):
    """Saves the generated PDF to GridFS."""
    try:
        fs = connect_to_gridfs()
        db = connect_to_mongo()
        
        with open(file_path, "rb") as file_data:
            file_id = fs.put(file_data, filename=file_name)
        
        os.remove(file_path)

        title = file_name
        metadata_dict = extract_metadata_pdf(file_path)  # Assuming this function exists

        if metadata_dict['title'] != "No title found":
            title = metadata_dict['title']
            existing_file = fs.find_one({'filename': title})
            if existing_file:
                fs.delete(file_id)
                raise Exception('File already exists')

        db.fs.files.update_one({'_id': file_id}, {'$set': {'filename': title}})

        return file_id, title
    except Exception as e:
        logger.error(f"Error saving PDF to GridFS: {e}")
        raise

