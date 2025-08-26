import pyassimp
import os
import sys
from os.path import join
from dotenv import load_dotenv

# === Configuración ===
DEFAULT_INPUT = "../resources/models/Christmas_Hat.fbx"
DEFAULT_OUTPUT = "../resources/models/Christmas_Hat.smd"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(join(SCRIPT_DIR, '../.env'))

# Asume que 'path_models_fbx' está configurado en tu .env
path_models_fbx = os.getenv('path_models_fbx')

# ===============================
# Exportador a SMD
# ===============================
def export_smd(scene, output_path):
    """
    Exporta la escena de pyassimp a un archivo SMD, ignorando los materiales.
    """
    with open(output_path, "w") as f:
        f.write("version 1\n")

        # Escribimos el nodo raíz
        f.write("nodes\n")
        f.write(" 0 \"root\" -1\n")
        f.write("end\n")

        # Escribimos el esqueleto (un solo hueso para el modelo estático)
        f.write("skeleton\n")
        f.write(" time 0\n")
        f.write(" 0 0.0 0.0 0.0 0 0 0\n")
        f.write("end\n")

        # Escribimos los triángulos del modelo
        f.write("triangles\n")

        # Iteramos sobre cada malla en la escena
        for mesh in scene.meshes:
            # Dado que hemos eliminado la lógica de materiales,
            # usamos un nombre de textura por defecto.
            mat_texture_name = "default_texture"
            
            for face in mesh.faces:
                # Aseguramos que la cara sea un triángulo
                if len(face) != 3:
                    continue

                # Escribimos el nombre de la textura para cada triángulo
                f.write(f"{mat_texture_name}\n")
                for idx in face:
                    v = mesh.vertices[idx]
                    n = mesh.normals[idx] if mesh.normals.any() else [0.0, 0.0, 1.0]
                    uv = [0.0, 0.0]
                    
                    # Verificamos si hay coordenadas de textura
                    if mesh.texturecoords is not None and len(mesh.texturecoords) > 0 and len(mesh.texturecoords[0]) > idx:
                        uv = mesh.texturecoords[0][idx][:2]

                    f.write(f" 0 {v[0]} {v[1]} {v[2]} {n[0]} {n[1]} {n[2]} {uv[0]} {uv[1]}\n")

        f.write("end\n")


# ===============================
# Conversión
# ===============================
def convert_to_smd(input_path, output_path):
    """
    Carga el modelo y lo exporta a SMD.
    """
    print(f"[INFO] Cargando modelo: {input_path}")
    try:
        scene = pyassimp.load(input_path)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo: {e}")
        return

    print(f"[INFO] {len(scene.meshes)} mallas encontradas.")

    export_smd(scene, output_path)
    pyassimp.release(scene)

    print(f"[OK] Exportado a SMD: {output_path}")


# ===============================
# Main
# ===============================
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        # Si no se proporciona una ruta, usamos la predeterminada
        input_path = DEFAULT_INPUT
        output_path = DEFAULT_OUTPUT

    # Aseguramos que la ruta de entrada sea la correcta
    full_input_path = join(SCRIPT_DIR, input_path)
    
    # Comprobamos si la ruta de entrada existe antes de intentar cargarla
    if not os.path.exists(full_input_path):
        # Si la ruta no existe, intentamos usar la ruta del .env si está disponible
        if path_models_fbx:
            full_input_path = join(path_models_fbx, os.path.basename(full_input_path))
            if not os.path.exists(full_input_path):
                print(f"[ERROR] No existe el archivo {full_input_path}. Por favor, verifica la ruta.")
                sys.exit(1)
        else:
            print(f"[ERROR] No existe el archivo {full_input_path} y la variable 'path_models_fbx' no está definida.")
            sys.exit(1)

    convert_to_smd(full_input_path, output_path)
