from django.urls import path
from .views import view_docs, add_doc
from . import views

urlpatterns = [
    path('view-docs', views.view_docs, name = 'view_docs'), #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
]