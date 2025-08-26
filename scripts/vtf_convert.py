import subprocess
import os 
from os.path import join
from dotenv import load_dotenv

# Obtener la ruta relativa del script.
SCRIPT_vtf_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar las variables de entorno desde el archivo .env
load_dotenv(join(SCRIPT_vtf_DIR, '../.env'))

# Obtener la variable de entorno de las texturas.
textures_relative_path = os.getenv("textures_relative_path")

# Obtener la variable de entorno de la libreria VTF
libs_relative_path = os.getenv("lib_vtf_relative_path")

# Construir la ruta completa a la libreria VTF
libs_absolute_path = join(SCRIPT_vtf_DIR, '../', libs_relative_path)

# Construimos la ruta a las texturas.
textures_absolute_path = join(SCRIPT_vtf_DIR, '../', textures_relative_path)

# Construir las rutas absolutas para los archivos de entrada y salida
input_file_path = join(textures_absolute_path, 'test.png')

# output_file_path = join(textures_absolute_path, 'test.vtf')
#
# El output_file_path es relativo a la ruta donde se lee el archivo antes de la conversion.


# Comando para convertir la imagen con rutas absolutas

resultado = subprocess.run(
    ['wine', join(libs_absolute_path, 'VTFCmd.exe'), '-file', input_file_path , '-rclampwidth' , '4096' , '-rclampheight' , '4096' , '-resize'],
    capture_output=True,
    text=True
)

# Imprimir la salida estándar y los errores
print("Salida estándar:", resultado.stdout)
print("Errores:", resultado.stderr)
print("Código de retorno:", resultado.returncode)


# Ahora creamos el vmt del material.

