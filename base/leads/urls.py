from django.urls import path
from . import views
from leads.views import AssignLeadView

urlpatterns = [
    path('', views.LeadsTableView.as_view(), name='leads_table'),
    path('assign_lead_multiple/', AssignLeadView.as_view(), {'methods': ['post_multiple_leads']}, name='assign_lead_multiple'),

]
