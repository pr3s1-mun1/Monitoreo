from django.urls import path
from . import views

urlpatterns = [
    path('', views.VLANListView.as_view(), name='list_vlans'),
    path('vlan/crear/', views.VlanCreateView.as_view(), name='create_vlan'),
    path('vlan/<int:pk>/actualizar/', views.VlanUpdateView.as_view(), name='update_vlan'),
    path('vlan/<int:pk>/eliminar/', views.VlanDeleteView.as_view(), name='delete_vlan'),

    path('ips/', views.IPSListView.as_view(), name='list_ips'),
]