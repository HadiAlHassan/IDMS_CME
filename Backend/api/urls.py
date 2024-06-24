from django.urls import path
from api import views  
from Pdf import pdf_handling
from WebScraping import WS_handling

urlpatterns = [ #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
    path('add-pdf', pdf_handling.add_pdf, name='add_pdf'),
    path('get-pdf-by-id/<file_id>/', pdf_handling.get_pdf_by_id, name='get_pdf_by_id'),
    path('get-pdf-by-name/<str:file_name>/',pdf_handling.get_pdf_by_name, name='get_pdf_by_name'),
    path('list-files/', pdf_handling.list_files, name='list_files'),
    path('handle-selected-pdfs', pdf_handling.handle_selected_pdfs, name='handle_selected_pdfs'),
    path('get_metadata_by_pdf_name', pdf_handling.get_metadata_by_pdf_name, name='get_metadata_by_pdf_name'),
    path('scrape-website', WS_handling.scrape_website, name='scrape_website'),
]