import os

# Definir la ruta exacta del archivo
ruta_wsgi = os.path.join('core', 'wsgi.py')

# El código exacto que requiere Django, estructurado línea por línea
contenido = [
    "import os",
    "import sys",
    "",
    "from django.core.wsgi import get_wsgi_application",
    "",
    "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')",
    "",
    "application = get_wsgi_application()",
]

# Escribir el archivo asegurando saltos de línea limpios y legibles para Windows
with open(ruta_wsgi, 'w', encoding='utf-8') as archivo:
    archivo.write("\n".join(contenido) + "\n")

print("--- REPARACIÓN EXITOSA ---")
print("El archivo core/wsgi.py ha sido reescrito directamente por Python.")