import os

# 1. Definir la estructura de carpetas
carpetas = [
    'core',
    'asistencia',
    'asistencia/migrations',
    'templates',
    'templates/asistencia',
    'static',
    'static/js',
    'static/images'
]

for carpeta in carpetas:
    os.makedirs(carpeta, exist_ok=True)
    print(f"✔ Carpeta creada: {carpeta}")

# 2. Contenidos de los archivos
archivos_codigo = {
    # ------ ARCHIVOS PRINCIPALES DEL PROYECTO ------
    'manage.py': """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("No se pudo importar Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",

    'core/__init__.py': '',
    'core/wsgi.py': """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
""",

    'core/settings.py': """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-expancore-asistencia-key-2026'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'asistencia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'asistencia.Trabajador'
LOGIN_URL = '/'
""",

    'core/urls.py': """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('asistencia.urls')),
]
""",

    # ------ ARCHIVOS DE LA APLICACIÓN DE ASISTENCIA ------
    'asistencia/__init__.py': '',
    'asistencia/migrations/__init__.py': '',
    
    'asistencia/models.py': """from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class TrabajadorManager(BaseUserManager):
    def create_user(self, numero_nomina, nombre_completo, password=None):
        if not numero_nomina:
            raise ValueError('Debe ingresar un número de nómina.')
        user = self.model(numero_nomina=numero_nomina, nombre_completo=nombre_completo)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_nomina, nombre_completo, password=None):
        user = self.create_user(numero_nomina, nombre_completo, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Trabajador(AbstractBaseUser):
    numero_nomina = models.CharField(max_length=20, unique=True, verbose_name="Número de Nómina")
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre Completo")
    puesto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Puesto")
    is_active = models.BooleanField(default=True, verbose_name="Activo / Permitir Ingreso")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = TrabajadorManager()

    USERNAME_FIELD = 'numero_nomina'
    REQUIRED_FIELDS = ['nombre_completo']

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return f"{self.numero_nomina} - {self.nombre_completo}"

    def has_perm(self, perm, obj=None): return self.is_superuser
    def has_module_perms(self, app_label): return self.is_superuser

class Actividad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Actividad")

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Catálogo de Actividades"

    def __str__(self):
        return self.nombre

class RegistroAsistencia(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador")
    actividad = models.ForeignKey(Actividad, on_delete=models.SET_NULL, null=True, verbose_name="Actividad")
    entrada = models.DateTimeField(auto_now_add=True, verbose_name="Hora de Entrada")
    salida = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Salida")

    class Meta:
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencias"

    def __str__(self):
        return f"{self.trabajador.nombre_completo} - {self.entrada.strftime('%Y-%m-%d')}"
""",

    'asistencia/admin.py': """from django.contrib import admin
import openpyxl
from django.http import HttpResponse
from .models import Trabajador, Actividad, RegistroAsistencia

@admin.action(description='Descargar registros seleccionados en Excel')
def descargar_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte Asistencias"
    headers = ['Número de Nómina', 'Trabajador', 'Puesto', 'Fecha', 'Hora Entrada', 'Hora Salida', 'Actividad']
    ws.append(headers)

    for r in queryset:
        ws.append([
            r.trabajador.numero_nomina,
            r.trabajador.nombre_completo,
            r.trabajador.puesto if r.trabajador.puesto else 'N/A',
            r.entrada.strftime('%Y-%m-%d'),
            r.entrada.strftime('%H:%M:%S'),
            r.salida.strftime('%H:%M:%S') if r.salida else 'En turno',
            r.actividad.nombre if r.actividad else 'N/A'
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte_Asistencia_Expancore.xlsx'
    wb.save(response)
    return response

class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('numero_nomina', 'nombre_completo', 'puesto', 'is_active')
    search_fields = ('numero_nomina', 'nombre_completo')
    list_filter = ('is_active',)
    def save_model(self, request, obj, form, change):
        if not change or form.initial.get('password') != obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha', 'hora_entrada', 'hora_salida', 'actividad')
    list_filter = ('entrada', 'actividad', 'trabajador')
    actions = [descargar_excel]
    def fecha(self, obj): return obj.entrada.strftime('%Y-%m-%d')
    def hora_entrada(self, obj): return obj.entrada.strftime('%H:%M:%S')
    def hora_salida(self, obj): return obj.salida.strftime('%H:%M:%S') if obj.salida else 'En Curso'

admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Actividad)
admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)
""",

    'asistencia/views.py': """from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Actividad, RegistroAsistencia

def login_trabajador(request):
    error = None
    if request.method == 'POST':
        nomina = request.POST.get('numero_nomina')
        password = request.POST.get('password')
        user = authenticate(request, username=nomina, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else: error = "Tu cuenta está suspendida temporalmente."
        else: error = "Número de nómina o contraseña incorrectos."
    return render(request, 'asistencia/login.html', {'error': error})

@login_required
def dashboard(request):
    trabajador = request.user
    actividades = Actividad.objects.all()
    turno_actual = RegistroAsistencia.objects.filter(trabajador=trabajador, salida__isnull=True).last()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'entrada' and not turno_actual:
            actividad_id = request.POST.get('actividad')
            act = Actividad.objects.get(id=actividad_id)
            RegistroAsistencia.objects.create(trabajador=trabajador, actividad=act)
        elif accion == 'salida' and turno_actual:
            turno_actual.salida = timezone.now()
            turno_actual.save()
        return redirect('dashboard')
    return render(request, 'asistencia/dashboard.html', {'trabajador': trabajador, 'actividades': actividades, 'turno_actual': turno_actual})

def logout_trabajador(request):
    logout(request)
    return redirect('login')
""",

    'asistencia/urls.py': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_trabajador, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_trabajador, name='logout'),
]
""",

    # ------ PLANTILLAS HTML VISTA MÓVIL ------
    'templates/asistencia/base.html': """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Expancore Asistencia</title>
    <link rel="manifest" href="/static/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen">
    <div class="w-full max-w-md min-h-screen bg-white shadow-xl flex flex-col justify-between">
        {% block content %}{% endblock %}
    </div>
    <script>
        if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/static/sw.js'); }
    </script>
</body>
</html>
""",

    'templates/asistencia/login.html': """{% extends 'asistencia/base.html' %}
{% block content %}
<div class="p-8 my-auto w-full">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-extrabold text-blue-900">EXPANCORE</h2>
        <p class="text-gray-500 text-sm">Control de Asistencia Laboral</p>
    </div>
    {% if error %}<div class="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-xs font-bold">{{ error }}</div>{% endif %}
    <form method="POST">
        {% csrf_token %}
        <div class="mb-4">
            <label class="block text-gray-700 text-xs font-bold mb-2 uppercase">Número de Nómina</label>
            <input type="text" name="numero_nomina" required class="w-full px-4 py-3 border rounded-xl focus:outline-blue-600 bg-gray-50">
        </div>
        <div class="mb-6">
            <label class="block text-gray-700 text-xs font-bold mb-2 uppercase">Contraseña</label>
            <input type="password" name="password" required class="w-full px-4 py-3 border rounded-xl focus:outline-blue-600 bg-gray-50">
        </div>
        <button type="submit" class="w-full bg-blue-950 text-white py-4 rounded-xl font-bold uppercase tracking-wider shadow-md">Ingresar</button>
    </form>
</div>
{% endblock %}
""",

    'templates/asistencia/dashboard.html': """{% extends 'asistencia/base.html' %}
{% block content %}
<div class="p-6 w-full flex-grow">
    <div class="bg-gradient-to-r from-blue-900 to-indigo-950 text-white p-5 rounded-2xl mb-6 shadow-md">
        <p class="text-[10px] uppercase tracking-widest opacity-75">Empleado Autorizado</p>
        <h3 class="text-xl font-bold mt-1">{{ trabajador.nombre_completo }}</h3>
        <p class="text-xs opacity-90 mt-1">Nómina: {{ trabajador.numero_nomina }} | Puesto: {{ trabajador.puesto|default:"Operativo" }}</p>
    </div>

    <div class="border border-gray-200 rounded-2xl p-6 text-center bg-gray-50">
        {% if not turno_actual %}
            <h4 class="text-gray-800 font-bold mb-4 text-sm uppercase tracking-wide">Marcar Entrada de Jornada</h4>
            <form method="POST">
                {% csrf_token %}
                <input type="hidden" name="accion" value="entrada">
                <select name="actividad" required class="w-full p-4 border rounded-xl mb-4 bg-white focus:outline-blue-600 font-medium text-sm text-gray-700">
                    <option value="">-- Selecciona Actividad --</option>
                    {% for act in actividades %}
                        <option value="{{ act.id }}">{{ act.nombre }}</option>
                    {% endfor %}
                </select>
                <button type="submit" class="w-full bg-emerald-600 text-white py-4 rounded-xl font-bold tracking-wider shadow-lg uppercase text-sm">Registrar Entrada</button>
            </form>
        {% else %}
            <h4 class="text-gray-800 font-bold mb-3 text-sm uppercase tracking-wide">Turno Activo</h4>
            <div class="bg-amber-50 border border-amber-200 text-amber-900 text-xs p-4 rounded-xl mb-5 text-left leading-relaxed">
                Actividad asignada: <strong class="text-amber-950 text-sm block mt-0.5">{{ turno_actual.actividad.nombre }}</strong>
                Iniciado a las: <span class="font-bold">{{ turno_actual.entrada|date:"H:i" }} hrs</span>
            </div>
            <form method="POST">
                {% csrf_token %}
                <input type="hidden" name="accion" value="salida">
                <button type="submit" class="w-full bg-rose-600 text-white py-4 rounded-xl font-bold tracking-wider shadow-lg uppercase text-sm">Registrar Salida</button>
            </form>
        {% endif %}
    </div>
</div>
<div class="p-4 border-t bg-gray-50 text-center rounded-b-xl">
    <a href="{% url 'logout' %}" class="text-xs text-rose-600 font-bold uppercase tracking-wider">Cerrar Sesión</a>
</div>
{% endblock %}
""",

    # ------ ARCHIVOS DE CONFIGURACIÓN PWA MÓVIL ------
    'static/manifest.json': """{
  "short_name": "Asistencia",
  "name": "Expancore Asistencia",
  "start_url": "/",
  "background_color": "#ffffff",
  "theme_color": "#1E3A8A",
  "display": "standalone",
  "orientation": "portrait",
  "icons": [
    { "src": "/static/images/icon.png", "type": "image/png", "sizes": "192x192" }
  ]
}""",

    'static/sw.js': """self.addEventListener('install', e => {
  e.waitUntil(caches.open('v1').then(cache => cache.addAll(['/', '/static/manifest.json'])));
});
self.addEventListener('fetch', e => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});""",

    # ------ SCRIPT DE CARGA DE TUS 28 TRABAJADORES ------
    'cargar_empleados.py': """import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from asistencia.models import Trabajador

empleados_oficiales = [
    {"nomina": "60379", "nombre": "CORNELIO GARCIA HERNANDEZ"},
    {"nomina": "113556", "nombre": "DOMITILO HERNANDEZ TORRES"},
    {"nomina": "113605", "nombre": "JHONNY LEON TORRES"},
    {"nomina": "113880", "nombre": "HUMBERTO JUAREZ VAZQUEZ"},
    {"nomina": "113881", "nombre": "JOSE ALFREDO BAUTISTA DE LA CRUZ"},
    {"nomina": "113956", "nombre": "CANDELARIO MAGAÑA GARCIA"},
    {"nomina": "115580", "nombre": "JOSE MORALES GARCIA"},
    {"nomina": "116329", "nombre": "ADRIAN EDUARDO MAGAÑA BAUTISTA"},
    {"nomina": "117355", "nombre": "JOSUE SANCHEZ GARCIA"},
    {"nomina": "117614", "nombre": "JOSE DAVID GARCIA HERNANDEZ"},
    {"nomina": "117635", "nombre": "MANUEL MALDONADO TORRES"},
    {"nomina": "118761", "nombre": "JUAN CARLOS VIDAL REYES"},
    {"nomina": "121171", "nombre": "JESUS SALVADOR HERNANDEZ"},
    {"nomina": "121333", "nombre": "ARDENZO GOMEZ PERERA"},
    {"nomina": "121680", "nombre": "ANTONIO PEREZ MAGAÑA"},
    {"nomina": "121848", "nombre": "WILLIAM PEREZ SALVADOR"},
    {"nomina": "122363", "nombre": "CARLOS VALENCIA HERNANDEZ"},
    {"nomina": "122631", "nombre": "JOSE GILDARDO HERNANDEZ HERNANDEZ"},
    {"nomina": "122849", "nombre": "EFREN PEREZ JIMENEZ"},
    {"nomina": "122999", "nombre": "ENRIQUE HERNANDEZ MORALES"},
    {"nomina": "123100", "nombre": "ANDRES PEREZ SANCHEZ"},
    {"nomina": "124082", "nombre": "JESUS IVAN HERNANDEZ HERNANDEZ"},
    {"nomina": "125029", "nombre": "EDUARDO DANIEL MONTEJO GARCIA"},
    {"nomina": "125032", "nombre": "ANGEL ROGELIO GARCIA DEARCIA"},
    {"nomina": "125033", "nombre": "RODRIGO VALENCIA GARCIA"},
    {"nomina": "125563", "nombre": "JADIEL DAMIAN RAMOS"},
    {"nomina": "130696", "nombre": "EDUARDO SANCHEZ HERNANDEZ"},
    {"nomina": "132651", "nombre": "ERICK GILBERTO GARCIA ARIAS"},
]

def importar():
    for emp in empleados_oficiales:
        t, creado = Trabajador.objects.get_or_create(
            numero_nomina=emp["nomina"],
            defaults={"nombre_completo": emp["nombre"]}
        )
        if creado:
            t.set_password("Expancore2026*")
            t.save()
    print("✔ Los 28 empleados oficiales han sido cargados con la clave: Expancore2026*")

if __name__ == '__main__':
    importar()
"""
}

# 3. Escribir el código en cada archivo correspondiente
for ruta, contenido in archivos_codigo.items():
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido.strip() + "\")
    print(f"✔ Archivo escrito con éxito: {ruta}")

print("\🚀 ESTRUCTURA COMPLETA GENERADA CON ÉXITO. YA PUEDES CORRER TUS MIGRACIONES.")
