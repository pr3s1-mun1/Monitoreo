from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import VLAN, IPS
from .forms import VLANForm, IPSForm

# Create your views here.
class VLANListView(ListView):
    model = VLAN    
    template_name = 'VLANS/lista_vlan.html'
    context_object_name = 'vlans'

class VlanCreateView(CreateView):
    model = VLAN
    form_class = VLANForm
    template_name = 'VLANS/form_vlan.html'
    success_url = reverse_lazy('list_vlans')

class VlanUpdateView(UpdateView):
    model = VLAN
    form_class = VLANForm
    template_name = 'VLANS/form_vlan.html'
    success_url = reverse_lazy('list_vlans')

class VlanDeleteView(DeleteView):
    model = VLAN
    template_name = 'VLANS/vlan_confirm_delete.html'
    success_url = reverse_lazy('list_vlans')

class IPSListView(ListView):
    model = IPS
    template_name = 'lookup_ip.html'
    context_object_name = 'ips'

    def get_queryset(self):
        ip = self.request.GET.get('ip')

        if ip:
            return IPS.objects.filter(ip__icontains=ip)
        
        return IPS.objects.none() 

class IPSCreateView(CreateView):
    model = IPS
    form_class = IPSForm
    template_name = 'form_ip.html'
    success_url = reverse_lazy('list_ips')