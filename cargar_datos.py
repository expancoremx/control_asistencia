import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from asistencia.models import Trabajador
from django.contrib.auth.hashers import make_password

empleados = [
    ("60379", "CORNELIO GARCIA HERNANDEZ"), ("113556", "DOMITILO HERNANDEZ TORRES"),
    ("113605", "JHONNY LEON TORRES"), ("113880", "HUMBERTO JUAREZ VAZQUEZ"),
    ("113881", "JOSE ALFREDO BAUTISTA DE LA CRUZ"), ("113956", "CANDELARIO MAGAÑA GARCIA"),
    ("115580", "JOSE MORALES GARCIA"), ("116329", "ADRIAN EDUARDO MAGAÑA BAUTISTA"),
    ("117355", "JOSUE SANCHEZ GARCIA"), ("117614", "JOSE DAVID GARCIA HERNANDEZ"),
    ("117635", "MANUEL MALDONADO TORRES"), ("118761", "JUAN CARLOS VIDAL REYES"),
    ("121171", "JESUS SALVADOR HERNANDEZ"), ("121333", "ARDENZO GOMEZ PERERA"),
    ("121680", "ANTONIO PEREZ MAGAÑA"), ("121848", "WILLIAM PEREZ SALVADOR"),
    ("122363", "CARLOS VALENCIA HERNANDEZ"), ("122631", "JOSE GILDARDO HERNANDEZ HERNANDEZ"),
    ("122849", "EFREN PEREZ JIMENEZ"), ("122999", "ENRIQUE HERNANDEZ MORALES"),
    ("123100", "ANDRES PEREZ SANCHEZ"), ("124082", "JESUS IVAN HERNANDEZ HERNANDEZ"),
    ("125029", "EDUARDO DANIEL MONTEJO GARCIA"), ("125032", "ANGEL ROGELIO GARCIA DEARCIA"),
    ("125033", "RODRIGO VALENCIA GARCIA"), ("125563", "JADIEL DAMIAN RAMOS"),
    ("130696", "EDUARDO SANCHEZ HERNANDEZ"), ("132651", "ERICK GILBERTO GARCIA ARIAS")
]

for nomina, nombre in empleados:
    user, created = Trabajador.objects.get_or_create(username=nomina)
    user.numero_nomina = nomina
    user.nombre_completo = nombre
    user.password = make_password('Alen01')
    user.save()
    print(f'Procesado: {nombre}')
print('Carga finalizada.')
