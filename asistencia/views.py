from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from .models import Trabajador, RegistroAsistencia
import pandas as pd

# --- Autenticación ---
def login_trabajador(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        passw = request.POST.get('password')
        usuario = authenticate(request, username=user, password=passw)
        if usuario is not None:
            login(request, usuario)
            return redirect('panel_admin') if usuario.is_staff else redirect('dashboard')
    return render(request, 'asistencia/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- Panel Empleado ---
@login_required
def dashboard(request):
    hoy = timezone.now().date()
    registro_hoy = RegistroAsistencia.objects.filter(trabajador=request.user, entrada__date=hoy).first()
    registro_abierto = registro_hoy if (registro_hoy and not registro_hoy.salida) else None
    registro_completado = registro_hoy if (registro_hoy and registro_hoy.salida) else None
    return render(request, 'asistencia/dashboard.html', {'registro_abierto': registro_abierto, 'registro_completado': registro_completado})

@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        hoy = timezone.now()
        registro_existente = RegistroAsistencia.objects.filter(trabajador=request.user, entrada__date=hoy.date()).first()
        if registro_existente and not registro_existente.salida:
            registro_existente.salida = hoy
            registro_existente.save()
        elif not registro_existente:
            RegistroAsistencia.objects.create(trabajador=request.user, entrada=hoy)
    return redirect('dashboard')

@login_required
def cambiar_mi_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'asistencia/cambiar_password.html', {'form': form})

# --- Administración ---
@staff_member_required
def panel_administrador(request):
    trabajadores = Trabajador.objects.filter(is_superuser=False)
    f_inicio = request.GET.get('fecha_inicio')
    f_fin = request.GET.get('fecha_fin')
    registros = RegistroAsistencia.objects.all().order_by('-entrada')
    if f_inicio and f_fin:
        registros = registros.filter(entrada__date__range=[f_inicio, f_fin])
    return render(request, 'asistencia/panel_admin.html', {'trabajadores': trabajadores, 'registros': registros, 'f_inicio': f_inicio, 'f_fin': f_fin})

@staff_member_required
def exportar_excel(request):
    f_inicio = request.GET.get('fecha_inicio')
    f_fin = request.GET.get('fecha_fin')
    qs = RegistroAsistencia.objects.all().order_by('-entrada')
    if f_inicio and f_fin:
        qs = qs.filter(entrada__date__range=[f_inicio, f_fin])
    data = list(qs.values('trabajador__username', 'trabajador__nombre_completo', 'entrada', 'salida'))
    if not data: return HttpResponse('No hay registros.')
    df = pd.DataFrame(data)
    for col in ['entrada', 'salida']:
        if col in df.columns: df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if x is not None else None)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte.xlsx"'
    df.to_excel(response, index=False)
    return response

@staff_member_required
def eliminar_registro(request, id):
    get_object_or_404(RegistroAsistencia, id=id).delete()
    return redirect('panel_admin')

@staff_member_required
def suspender_trabajador(request, id):
    t = get_object_or_404(Trabajador, id=id)
    t.is_active = not t.is_active
    t.save()
    return redirect('panel_admin')
