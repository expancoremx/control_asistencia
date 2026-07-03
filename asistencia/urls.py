from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_trabajador, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/', views.panel_administrador, name='panel_admin'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('eliminar/<int:id>/', views.eliminar_registro, name='eliminar_registro'),
    path('suspender/<int:id>/', views.suspender_trabajador, name='suspender_trabajador'),
    path('registrar/', views.registrar_asistencia, name='registrar_asistencia'),
    path('cambiar-pass/', views.cambiar_mi_contrasena, name='cambiar_mi_contrasena'),
]
