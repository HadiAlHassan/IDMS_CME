from initializations.initializer import cohere_api_key
from rest_framework.response import Response
from rest_framework.decorators import api_view
import cohere
from Utils.decorators import timing_decorator
from fpdf import FPDF
import os
from pymongo import MongoClient
from gridfs import GridFS
from django.utils import timezone
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

co = cohere.Client(api_key=cohere_api_key)

preamble = """you are a legal llm,  made to assist the client in their legal tasks.
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
    author = "CohereLLM"

    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
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

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    textfile_name = f"{file_name}.txt"
    with open(textfile_name, "w", encoding='utf-8') as file:
        file.write(response_text)

    with open(textfile_name, "r", encoding='utf-8') as file:
        for line in file:
            if pdf.get_y() > 260:  # Check if we are at the bottom of the page
                pdf.add_page()
            pdf.multi_cell(0, 10, txt=line, align='L')

    directory = os.getcwd()
    os.remove(f"{directory}/{textfile_name}")

    pdf_file_name = f"{file_name}.pdf"
    pdf.output(pdf_file_name)

    # Save PDF to MongoDB using GridFS
    fs = connect_to_gridfs()
    with open(pdf_file_name, "rb") as pdf_file:
        file_id = fs.put(pdf_file, filename=pdf_file_name, author=author)
    
    os.remove(pdf_file_name)

    # Save metadata in the generated_files collection
    db = connect_to_mongo()
    generated_file_data = {
        '_id': file_id,
        'file_name': pdf_file_name,
        'author': author,
        'date_created': timezone.now(),
    }
    db['generated_files'].insert_one(generated_file_data)

    return Response({'response': response_text, 'file_id': str(file_id)}, status=200)
