import os
from os.path import join
from dotenv import load_dotenv

# Obtener la ruta relativa del script.
SCRIPT_vtm_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar las variables de entorno desde el archivo .env
load_dotenv(join(SCRIPT_vtm_DIR, '../.env'))

# Funcion para crear el convertidor a vmt.

def crear_vmt(**kwargs):
    