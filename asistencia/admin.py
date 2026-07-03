from django.contrib import admin
from .models import Trabajador, Actividad, RegistroAsistencia

# Filtramos para que no aparezcan los superusuarios en la lista de trabajadores
@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('numero_nomina', 'nombre_completo', 'puesto')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'entrada', 'salida')
    list_filter = ('trabajador', 'entrada')
