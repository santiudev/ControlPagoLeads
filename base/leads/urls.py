from django.urls import path
from . import views
from closer.views import CloserStatsView

urlpatterns = [
    path('', views.LeadsTableView.as_view(), name='leads_table'),
    path('closer_stats/', CloserStatsView.as_view(), name='closer_stats'),
    
]
