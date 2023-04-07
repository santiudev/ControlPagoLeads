
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Lead
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.utils import timezone



User = get_user_model()
class LeadsTableView(LoginRequiredMixin, View):
    template_name = 'table.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        option = request.GET.get('option')

        if request.user.is_superuser:
            leads = Lead.objects.all()
            closers = User.objects.all()
        else:
            leads = Lead.objects.filter(closer=request.user)
            closers = []

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
        
        return render(request, self.template_name, {'leads': leads, 'closer_name': closer_name, 'is_admin': request.user.is_superuser, 'closers': closers})

    def post(self, request, *args, **kwargs):
        lead_id = request.POST.get('lead_id')
        action = request.POST.get('action')

        if action == 'contact':
            lead = Lead.objects.get(id=lead_id)
            lead.contacted = not lead.contacted
            lead.save()
            return JsonResponse({'status': 'success', 'contacted': lead.contacted})

logger = logging.getLogger(__name__)
class AssignSingleLeadView(LoginRequiredMixin, View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        lead_id = request.POST.get('lead_id')
        closer_id = request.POST.get('closer_id')

        lead = Lead.objects.get(id=lead_id)
        closer = User.objects.get(id=closer_id)
        lead.closer = closer
        lead.save()

        return JsonResponse({'status': 'success'})
    


class AssignMultipleLeadsView(LoginRequiredMixin, View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        lead_ids = request.POST.getlist('lead_ids[]')
        closer_id = request.POST.get('closer_id')

        print(f"lead_ids: {lead_ids}")
        print(f"closer_id: {closer_id}")
        closer = User.objects.get(id=closer_id)

        for lead_id in lead_ids:
            lead = Lead.objects.filter(id=lead_id).first()
            if lead is not None:
                lead.closer = closer
                lead.save()
            else:
                logger.error(f"No se encontró el objeto Lead con id = {lead_id}")

        return JsonResponse({'status': 'success'})
    
    
@csrf_exempt
@require_POST
def handle_webhook(request):
    # Procesa los datos del webhook aquí
    data = json.loads(request.body)
    print(data)
    buyer_name = data['data']['buyer']['name']
    
    phone_number = data['data']['buyer']['checkout_phone']
    payment_status = data['data']['purchase']['status']

    # Lista de estados de pago válidos
    valid_payment_statuses = ['BLOCKED', 'CANCELLED', 'CHARGEBACK', 'NO_FUNDS', 'PRINTED_BILLET', 'PROTESTED', 'UNDER_ANALISYS', 'WAITING_PAYMENT']

    # Verifica si el payment_status es válido
    if payment_status in valid_payment_statuses:
    #Guarda la data en modelo Lead
        lead = Lead(
            nombre=buyer_name,
            fecha_hora=timezone.datetime.now(),

            numero=phone_number,
            error=payment_status
        )
        lead.save()
    # Devuelve una respuesta de éxito
    return JsonResponse({"status": "success"})



