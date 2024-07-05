from django.urls import path
from api import views  
from Pdf import pdf_handling
from WebScraping import WS_handling
from gen_ai import chat_bot, rag
from users import user_functions

urlpatterns = [ #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
    path('add-pdf', pdf_handling.add_pdf, name='add_pdf'),
    path('get-pdf-by-id/<file_id>/', pdf_handling.get_pdf_by_id, name='get_pdf_by_id'),
    path('get-pdf-by-name/<str:file_name>/',pdf_handling.get_pdf_by_name, name='get_pdf_by_name'),
    path('list-pdfs/', pdf_handling.list_pdfs, name='list_pdfs'),
    path('handle-selected-pdfs', pdf_handling.handle_selected_pdfs, name='handle_selected_pdfs'),
    path('get_metadata_by_pdf_name', pdf_handling.get_metadata_by_pdf_name, name='get_metadata_by_pdf_name'),
    path('scrape-website', WS_handling.scrape_website, name='scrape_website'),
    path('chat-bot', chat_bot.chatbot, name='chat_bot'),
    path('get-all-metadata',pdf_handling.get_all_metadata, name="get_all_metadata"),
    path('category-document-count', pdf_handling.category_document_count, name='category_document_count'),
    path('signup', user_functions.signup, name='signup'),
    path('login', user_functions.login, name='login'),
    path('get-news', WS_handling.get_news, name="get_news"),
    path('rag', rag.rag, name='rag')
]