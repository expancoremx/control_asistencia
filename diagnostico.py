import os
import sys

print("--- DIAGNÓSTICO DE ENTORNO EXPANCORE ---")
print(f"Ruta actual de ejecución: {os.getcwd()}")
print(f"Versión de Python: {sys.version}\n")

# Verificar qué carpetas existen realmente
if os.path.exists('core'):
    print("✔ La carpeta 'core' SÍ existe en esta ruta.")
    archivos = os.listdir('core')
    print(f"Archivos dentro de 'core': {archivos}")
    
    if 'wsgi.py' in archivos:
        print("✔ 'wsgi.py' existe. Leyendo su contenido interno real:")
        with open('core/wsgi.py', 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("❌ ERROR: 'wsgi.py' NO está en la carpeta core o tiene otro nombre.")
else:
    print("❌ ERROR CRÍTICO: La carpeta 'core' no existe en este directorio actual.")