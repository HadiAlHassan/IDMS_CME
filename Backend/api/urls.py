from django.urls import path
from . import views

urlpatterns = [
    path('view-docs', views.view_docs, name = 'view_docs'), #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
    path('add-pdf', views.add_pdf, name='add_pdf'),
    path('get-pdf-by-id/<file_id>/', views.get_pdf_by_id, name='get_pdf_by_id'),
    path('get-pdf-by-name/<str:file_name>/', views.get_pdf_by_name, name='get_pdf_by_name'),
    path('list-files/', views.list_files, name='list_files'),
    path('handle-selected-pdfs', views.handle_selected_pdfs, name='handle_selected_pdfs'),
    path('get_metadata_by_pdf_name', views.get_metadata_by_pdf_name, name='get_metadata_by_pdf_name'),
    path('scrape-website', views.scrape_website, name='scrape_website'),
]