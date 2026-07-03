import os

# 1. Reescribir manage.py para forzar la compatibilidad de rutas con Python 3.14
manage_content = """#!/usr/bin/env python
import os
import sys

def main():
    # Insertar la carpeta actual en las rutas del sistema para corregir Python 3.14
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("No se pudo importar Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

with open('manage.py', 'w', encoding='utf-8') as f:
    f.write(manage_content.strip() + "\\n")

# 2. Asegurar el contenido de core/wsgi.py de forma exacta
wsgi_content = """import os
import sys

# Forzar la ruta del proyecto también en el WSGI
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
"""

with open('core/wsgi.py', 'w', encoding='utf-8') as f:
    f.write(wsgi_content.strip() + "\\n")

print("✔ Parche de compatibilidad aplicado a manage.py y core/wsgi.py con éxito.")