from django.db import models

class Servidor(models.Model): 
    nombre = models.CharField(max_length=100) 
    ip = models.GenericIPAddressField(protocol='IPv4') 
    servicio = models.CharField(blank=True, null=True) 
    referencia = models.CharField(max_length=100, null=True, blank=True) 
    referencia2 = models.CharField(max_length=100, null=True, blank=True) 
    icono = models.ForeignKey('Iconos', on_delete=models.CASCADE, null=True) 
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE) 
    proveedor = models.CharField(max_length=100, null=True, blank=True) 
    puerto = models.IntegerField(null=True, blank=True)
    def __str__(self): return f"{self.nombre} ({self.ip})"

class Iconos(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=70)
    ruta = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.descripcion})"
    

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=70, null=True)

    def __str__(self):
        return f"{self.nombre}"
    
ESTATUS_CHOICES = [
    (1, 'Activo'),
    (2, 'Cerrado'),
]

class Reportes(models.Model):
    nombre = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='IPv4')
    enlace = models.IntegerField(null=True, blank=True)
    servicio = models.CharField(max_length=100, null=True, blank=True)
    que_cayo = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_levanta = models.DateTimeField(null=True, blank=True)
    quien_levanta = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='quien_levanta')
    personal_sitio = models.CharField(max_length=100, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    estatus = models.IntegerField(choices=ESTATUS_CHOICES, default=1)
    observaciones_finales = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Reporte de {self.servidor.nombre} a las {self.fecha_hora}: {self.estado}"
    

class ReportesTelefonia(models.Model):
    sitio = models.CharField(max_length=100)
    referencia = models.CharField(max_length=50)
    contacto_sitio = models.CharField(max_length=50)
    numero_contacto = models.IntegerField()
    numero_reporte = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_levanta = models.DateTimeField(null=True, blank=True)
    descripcion_problema = models.CharField(max_length=100)
    quien_levanta = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='usuario_levanta')
    observaciones = models.TextField(null=True, blank=True)
    estatus = models.IntegerField(choices=ESTATUS_CHOICES, default=1)
    observaciones_finales = models.TextField(null=True, blank=True)
