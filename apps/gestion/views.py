# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Iconos, Servidor, Categoria, Reportes, ReportesTelefonia
from .forms import IconoForm, ServidorForm, CategoriaForm, ReporteForm, ReportesTelefoniaForm
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

# -------- Iconos -------- #

def lista_iconos(request):
    iconos = Iconos.objects.all()
    return render(request, 'iconos/lista.html', {'iconos': iconos})

def crear_icono(request):
    form = IconoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('iconos')
    return render(request, 'iconos/formulario.html', {'form': form})

def editar_icono(request, pk):
    icono = get_object_or_404(Iconos, pk=pk)
    form = IconoForm(request.POST or None, instance=icono)
    if form.is_valid():
        form.save()
        return redirect('iconos')
    return render(request, 'iconos/formulario.html', {'form': form})

def eliminar_icono(request, pk):
    icono = get_object_or_404(Iconos, pk=pk)
    if request.method == 'POST':
        icono.delete()
        return redirect('iconos')
    return render(request, 'iconos/eliminar.html', {'objeto': icono})

# -------- Servidores -------- #

def lista_servidores(request):
    servidores = Servidor.objects.all()
    return render(request, 'servidores/lista.html', {'servidores': servidores})

def crear_servidor(request):
    form = ServidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('servidores')
    return render(request, 'servidores/formulario.html', {'form': form})

def editar_servidor(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    form = ServidorForm(request.POST or None, instance=servidor)
    if form.is_valid():
        form.save()
        return redirect('servidores')
    return render(request, 'servidores/formulario.html', {'form': form})

def eliminar_servidor(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    if request.method == 'POST':
        servidor.delete()
        return redirect('servidores')
    return render(request, 'servidores/eliminar.html', {'objeto': servidor})

# -------- Categorías -------- #
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/formulario.html', {'form': form, 'titulo': 'Crear Categoría'})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/formulario.html', {'form': form, 'titulo': 'Editar Categoría'})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
    return render(request, 'categorias/eliminar.html', {
        'objeto': categoria,  # o puedes usar 'categoria' si así lo tienes en el template
        'tipo': 'Categoría'
    })

# -------- Reportes -------- #
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False) 
            reporte.quien_levanta = request.user  
            reporte.save()
            return redirect('reportes')
    else:
        form = ReporteForm()

    return render(request, 'reportes/formulario.html', {'form': form})

def lista_reportes(request):
    reportes = Reportes.objects.all().select_related('quien_levanta')

    q = request.GET.get('q')
    estatus = request.GET.get('estatus')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if q:
        reportes = reportes.filter(
            Q(nombre__icontains=q) |
            Q(ip__icontains=q) |
            Q(que_cayo__icontains=q) |
            Q(servicio__icontains=q)
        )

    if estatus in ['1', '2']:
        reportes = reportes.filter(estatus=int(estatus))

    if fecha_inicio:
        reportes = reportes.filter(fecha__date__gte=fecha_inicio)

    if fecha_fin:
        reportes = reportes.filter(fecha__date__lte=fecha_fin)

    reportes = reportes.order_by('-fecha')

    # Mapear IP -> proveedor
    servidores = Servidor.objects.all()
    ip_a_proveedor = {str(s.ip): s.proveedor for s in servidores}

    # Asignar proveedor a cada reporte
    for r in reportes:
        r.proveedor = ip_a_proveedor.get(str(r.ip), "Desconocido")

    return render(request, 'reportes/reportes.html', {
        'reportes': reportes
    })

# ------- Reportes Telefonía ------- #
def crear_reporte_telefonia(request):
    if request.method == 'POST':
        form = ReportesTelefoniaForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False) 
            reporte.quien_levanta = request.user  
            reporte.save()
            return redirect('gestionar_telefonia')
    else:
        form = ReportesTelefoniaForm()

    return render(request, 'reportes_telefonia/crear.html', {'form': form})

def editar_telefonia(request, id):
    reporte = get_object_or_404(ReportesTelefonia, id=id)

    if request.method == 'POST':
        form = ReportesTelefoniaForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('gestionar_telefonia')
    else:
        form = ReportesTelefoniaForm(instance=reporte)

    return render(request, 'reportes_telefonia/crear.html', {
        'form': form,
        'modo': 'editar',
        'reporte': reporte
    })

def lista_reportes_telefonia(request):
    reportes = ReportesTelefonia.objects.all().select_related('quien_levanta')
    reportes = reportes.order_by('-fecha')
    return render(request, 'reportes_telefonia/gestionar.html', {
        'reportes': reportes
    })

# === Endpoints === #
def obtener_servidor(request, ip):
    servidor = get_object_or_404(Servidor, ip=ip)
    data = {
        'nombre': servidor.nombre,
        'ip': servidor.ip,
        'servicio': servidor.servicio,
        'referencia': servidor.referencia,
        'referencia2': servidor.referencia2,
        'categoria': servidor.categoria.nombre,
        'icono': servidor.icono.ruta if servidor.icono else None,
    }
    return JsonResponse(data)

def guardar_reporte(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ip = request.POST.get('ip')
        enlace = request.POST.get('enlace')
        servicio = request.POST.get('servicio')
        que_cayo = request.POST.get('que_cayo')
        quien_levanta = request.user if request.user.is_authenticated else None
        personal_sitio = request.POST.get('personal_sitio')
        telefono_contacto = request.POST.get('telefono_contacto')
        observacion = request.POST.get('observacion')

        reporte = Reportes(
            nombre=nombre,
            ip=ip,
            enlace=enlace,
            servicio=servicio,
            que_cayo=que_cayo,
            quien_levanta=quien_levanta,
            personal_sitio=personal_sitio,
            telefono_contacto=telefono_contacto,
            observacion=observacion
        )
        reporte.save()
        return JsonResponse({'status': 'success'})
    
def cerrar_reporte(request, pk):
    observaciones_finales = request.POST.get('observaciones_finales', '')
    if request.method == 'POST':
        reporte = get_object_or_404(Reportes, pk=pk)
        reporte.observaciones_finales = observaciones_finales
        reporte.estatus = 2 
        reporte.fecha_levanta = timezone.now()
        reporte.save()
        return redirect('reportes')
    
def cerrar_telefonia(request, pk):
    observaciones_finales = request.POST.get('observaciones_finales', '')
    if request.method == 'POST':
        reporte = get_object_or_404(ReportesTelefonia, pk=pk)
        reporte.observaciones_finales = observaciones_finales
        reporte.estatus = 2 
        reporte.fecha_levanta = timezone.now()
        reporte.save()
        return redirect('gestionar_telefonia')