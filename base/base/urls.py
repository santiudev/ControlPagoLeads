from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView 
from leads.views import AssignSingleLeadView, AssignMultipleLeadsView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('closer.urls')),  
    path('', RedirectView.as_view(url='login/')),  
    path('leads/', include('leads.urls')),
    path('assign_lead/', AssignSingleLeadView.as_view(), name='assign_single_lead'),
    path('assign_lead_multiple/', AssignMultipleLeadsView.as_view(), name='assign_multiple_leads'),

    
]
