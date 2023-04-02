
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Lead
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



class LeadsTableView(LoginRequiredMixin, View):
    template_name = 'table.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        option = request.GET.get('option')
        leads = Lead.objects.all()

        if option == 'recent':
            leads = leads.order_by('-fecha_hora')
        elif option == 'old':
            leads = leads.order_by('fecha_hora')
        elif option == 'unassigned':
            leads = leads.filter(closer__isnull=True)
        elif option == 'assigned':
            leads = leads.exclude(closer__isnull=True)

        closer_name = None
        if request.user.is_authenticated and hasattr(request.user, 'closer'):
            closer_name = request.user.closer.name

        return render(request, self.template_name, {'leads': leads, 'closer_name': closer_name})

 
    def post(self, request, *args, **kwargs):
        lead_id = request.POST.get('lead_id')
        lead = Lead.objects.get(id=lead_id)
        if lead.closer:
            messages.error(request, 'Ya hay un Closer asignado a este lead.')
        else:
            lead.closer = request.user
            lead.save()
            messages.success(request, 'Lead asignado correctamente.')
        return self.get(request, *args, **kwargs)