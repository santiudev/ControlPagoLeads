from django.urls import path
from .views import CloserLoginView, CloserLogoutView, CloserStatsView

urlpatterns = [
    path('login/', CloserLoginView.as_view(), name='login'),
    path('logout/', CloserLogoutView.as_view(), name='logout'),
   
]
