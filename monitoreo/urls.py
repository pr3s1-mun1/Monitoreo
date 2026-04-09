from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('apps.panel.urls')),
    path('gestion/', include('apps.gestion.urls')),
    path('ip/', include('apps.cat_vlan.urls')),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
