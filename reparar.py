import os

# Forzar la creación de la carpeta core por si acaso
os.makedirs('core', exist_ok=True)

# 1. Reescribir core/__init__.py completamente limpio
with open('core/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

# 2. Reescribir core/wsgi.py con el formato y saltos de línea correctos que exige Django
wsgi_contenido = [
    "import os",
    "from django.core.wsgi import get_wsgi_application",
    "",
    "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')",
    "",
    "application = get_wsgi_application()",
]

with open('core/wsgi.py', 'w', encoding='utf-8') as f:
    f.write("\n".join(wsgi_contenido) + "\n")

print("✔ Archivos internos purgados y restaurados con éxito.")