from django import forms
from .models import VLAN, IPS

class VLANForm(forms.ModelForm):
    class Meta:
        model = VLAN
        fields = ['numero','nombre', 'descripcion', 'red']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'red': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 192.168.10.0/24'
            }),
        }

class IPSForm(forms.ModelForm):
    class Meta:
        model = IPS
        fields = ['ip', 'asignado', 'departamento', 'tipo', 'tipo_ip', 'vlan', 'comentarios']
        widgets = {
            'ip': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }