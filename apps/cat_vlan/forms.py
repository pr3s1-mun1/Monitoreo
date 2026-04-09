from django import forms
from .models import VLAN, IPS

class VLANForm(forms.ModelForm):
    class Meta:
        model = VLAN
        fields = ['numero','nombre', 'descripcion']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IPSForm(forms.ModelForm):
    class Meta:
        model = IPS
        fields = ['ip', 'asignado', 'departamento', 'tipo', 'tipo_ip', 'vlan', 'comentarios']
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'asignado': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_ip': forms.Select(attrs={'class': 'form-control'}),
            'vlan': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }