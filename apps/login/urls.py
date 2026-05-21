from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.index, name='index'),  # tu vista protegida con login_required
]
