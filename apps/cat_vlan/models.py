from django.db import models

TIPOS_INTERNET = [
    ('Proxy', 'Proxy'),
    ('Directo', 'Directo'),
]

TIPO_IP = [
    ('Pública', 'Pública'),
    ('Privada', 'Privada'),
]

class IPS(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    asignado = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True, choices=TIPOS_INTERNET)
    tipo_ip = models.CharField(max_length=50, blank=True, null=True, choices=TIPO_IP)
    vlan = models.ForeignKey('VLAN', on_delete=models.SET_NULL, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ip} - VLAN: {self.vlan}"
    
class VLAN(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"VLAN {self.numero} - {self.nombre}"