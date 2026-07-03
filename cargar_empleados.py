import os
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
