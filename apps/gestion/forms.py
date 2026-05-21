# gestion/forms.py

from django import forms
from .models import Iconos, Servidor, Categoria, Reportes, ReportesTelefonia

class BootstrapFormMixin:
    """
    Aplica clases de Bootstrap a todos los campos del form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for nombre, field in self.fields.items():
            widget = field.widget

            if widget.__class__.__name__ in ['CheckboxInput']:
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

            # Placeholder opcional
            if hasattr(field, 'label'):
                widget.attrs['placeholder'] = field.label

class IconoForm(forms.ModelForm):
    class Meta:
        model = Iconos
        fields = ['nombre', 'descripcion', 'ruta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'descripcion': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'ruta': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full', 'placeholder': 'ruta del icono, ej: icons/server.png'}),
        }

class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nombre', 'ip', 'categoria', 'servicio', 'referencia', 'referencia2', 'proveedor', 'puerto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'ip': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'servicio': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full', 'type': 'number', 'inputmode': 'numeric', 'pattern': '[0-9]*'}),
            'referencia': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'referencia2': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'categoria': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'proveedor': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'puerto': forms.NumberInput(attrs={'class': 'border rounded px-3 py-2 w-full hidden'}),
            'icono': forms.Select(attrs={
                'class': 'hidden'
            }),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'descripcion': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['nombre', 'ip', 'enlace', 'servicio', 'que_cayo', 'personal_sitio', 'telefono_contacto', 'observacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'ip': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'enlace': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full', 'type': 'number', 'inputmode': 'numeric', 'pattern': '[0-9]*'}),
            'servicio': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full', 'type': 'number', 'inputmode': 'numeric', 'pattern': '[0-9]*'}),
            'que_cayo': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'personal_sitio': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'observacion': forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full', 'rows': 4}),
        }
        labels = {
            'enlace': 'Número de Sitio',
        }

class ReportesTelefoniaForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = ReportesTelefonia
        fields = [
            'sitio',
            'referencia',
            'contacto_sitio',
            'numero_contacto',
            'numero_reporte',
            'descripcion_problema',
            'observaciones',
        ]

        widgets = {
            'fecha_levanta': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'observaciones_finales': forms.Textarea(attrs={'rows': 3}),
        }