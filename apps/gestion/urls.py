from django.urls import path
from . import views

urlpatterns = [
    # Servidores
    path('servidores/', views.lista_servidores, name='servidores'),
    path('servidores/nuevo/', views.crear_servidor, name='crear_servidor'),
    path('servidores/editar/<int:pk>/', views.editar_servidor, name='editar_servidor'),
    path('servidores/eliminar/<int:pk>/', views.eliminar_servidor, name='eliminar_servidor'),

    # Iconos
    path('iconos/', views.lista_iconos, name='iconos'),
    path('iconos/nuevo/', views.crear_icono, name='crear_icono'),
    path('iconos/editar/<int:pk>/', views.editar_icono, name='editar_icono'),
    path('iconos/eliminar/<int:pk>/', views.eliminar_icono, name='eliminar_icono'),

    # Categorías
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/nuevo/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Reportes
    path('reportes/', views.lista_reportes, name='reportes'),
    path('reportes/nuevo/', views.crear_reporte, name='crear_reporte'),

    # Reportes Telefonía
    path('reportes_telefonia/nuevo', views.crear_reporte_telefonia, name='crear_telefonia'),
    path('reportes_telefonia/editar/<int:id>', views.editar_telefonia, name='editar_telefonia'),
    path('reportes_telefonia/', views.lista_reportes_telefonia, name='gestionar_telefonia'),

    # API Endpoints
    path('api/servidor/<str:ip>/', views.obtener_servidor, name='obtener_servidor'),
    path('api/guardar_reporte/', views.guardar_reporte, name='guardar_reporte'),
    path('api/cerrar_reporte/<int:pk>/', views.cerrar_reporte, name='cerrar_reporte'),
    path('api/cerrar_telefonia/<int:pk>/', views.cerrar_telefonia, name='cerrar_telefonia'),
]
