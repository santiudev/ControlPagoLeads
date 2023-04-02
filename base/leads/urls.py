from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeadsTableView.as_view(), name='leads_table'),
    
]
