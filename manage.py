#!/usr/bin/env python
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
