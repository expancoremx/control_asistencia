from django.db import models
from django.contrib.auth.models import AbstractUser

class Trabajador(AbstractUser):
    numero_nomina = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'numero_nomina'
    REQUIRED_FIELDS = ['nombre_completo', 'username']

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class RegistroAsistencia(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    entrada = models.DateTimeField(auto_now_add=True)
    salida = models.DateTimeField(null=True, blank=True)
