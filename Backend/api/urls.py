from django.urls import path
from . import views

urlpatterns = [
    path('view-docs', views.view_docs, name = 'view_docs'), #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
    path('add-pdf', views.add_pdf, name='add_pdf'),
    #path('api/get-pdf/<file_id>/', views.get_pdf, name='get_pdf'),
]