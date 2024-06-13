from django.urls import path
from .views import DocGeneralInfoView
from . import views

urlpatterns = [
    path('docs-info', DocGeneralInfoView.as_view()), #redirects to api/views.py
    path('add-doc', views.add_doc, name='add_doc'),
]