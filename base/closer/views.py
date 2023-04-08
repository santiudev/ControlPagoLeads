from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Closer
from leads.models import Lead



class CloserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/leads/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_navbar'] = True
        return context
    


class CloserLogoutView(LogoutView):
    next_page = 'login'



def closer_context(request):
    closer_name = None
    if request.user.is_authenticated and hasattr(request.user, 'closer'):
        closer_name = request.user.closer.name
    return {'closer_name': closer_name}

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect(reverse_lazy('leads_table'))

class CloserStatsView(AdminRequiredMixin, View):
    template_name = 'closer_stats.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        closers = Closer.objects.annotate(
            total_leads=Count('lead'),
            contacted_leads=Count('lead', filter=Q(lead__contacted=True))
        )
    
        return render(request, self.template_name, {'closers': closers})