import pyassimp
import os
import sys
import json
from os.path import join, dirname, abspath
from dotenv import load_dotenv

# === Configuración ===
SCRIPT_DIR = dirname(abspath(__file__))

JSON_LIST = join(SCRIPT_DIR, "../resources/temp/file_list.json")
INPUT_DIR = join(SCRIPT_DIR, "../resources/models/")
OUTPUT_DIR = join(SCRIPT_DIR, "../resources/exported/models/")

load_dotenv(join(SCRIPT_DIR, '../.env'))

# Asume que 'path_models_fbx' está configurado en tu .env (opcional)
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

        # Nodos
        f.write("nodes\n")
        f.write(" 0 \"root\" -1\n")
        f.write("end\n")

        # Esqueleto (único hueso raíz)
        f.write("skeleton\n")
        f.write(" time 0\n")
        f.write(" 0 0.0 0.0 0.0 0 0 0\n")
        f.write("end\n")

        # Triángulos
        f.write("triangles\n")

        for mesh in scene.meshes:
            mat_texture_name = "default_texture"

            for face in mesh.faces:
                if len(face) != 3:
                    continue

                f.write(f"{mat_texture_name}\n")
                for idx in face:
                    v = mesh.vertices[idx]
                    n = mesh.normals[idx] if mesh.normals.any() else [0.0, 0.0, 1.0]
                    uv = [0.0, 0.0]

                    if (
                        mesh.texturecoords is not None
                        and len(mesh.texturecoords) > 0
                        and len(mesh.texturecoords[0]) > idx
                    ):
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
        return False

    print(f"[INFO] {len(scene.meshes)} mallas encontradas.")

    try:
        export_smd(scene, output_path)
        pyassimp.release(scene)
    except Exception as e:
        print(f"[ERROR] Falló la exportación: {e}")
        return False

    print(f"[OK] Exportado a SMD: {output_path}")
    return True


# ===============================
# Main (Batch Processor)
# ===============================
if __name__ == "__main__":
    # Comprobar que existe la lista de archivos
    if not os.path.exists(JSON_LIST):
        print(f"[ERROR] No se encontró la lista de archivos: {JSON_LIST}")
        sys.exit(1)

    with open(JSON_LIST, "r") as f:
        try:
            file_list = json.load(f)
        except json.JSONDecodeError:
            print(f"[ERROR] {JSON_LIST} no contiene un JSON válido")
            sys.exit(1)

    if not isinstance(file_list, list):
        print(f"[ERROR] {JSON_LIST} debe contener una lista de nombres de archivos FBX")
        sys.exit(1)

    # Crear carpeta de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Listas de control
    success_list = []
    fail_list = []

    # Procesar cada archivo FBX
    for filename in file_list:
        fbx_path = join(INPUT_DIR, filename)
        if not os.path.exists(fbx_path):
            if path_models_fbx:
                fbx_path = join(path_models_fbx, filename)
            if not os.path.exists(fbx_path):
                print(f"[ERROR] No existe el archivo {fbx_path}. Saltando.")
                fail_list.append(filename)
                continue

        smd_name = os.path.splitext(filename)[0] + ".smd"
        smd_path = join(OUTPUT_DIR, smd_name)

        if convert_to_smd(fbx_path, smd_path):
            success_list.append(filename)
        else:
            fail_list.append(filename)

    # ===============================
    # Resumen final
    # ===============================
    print("\n========== RESUMEN ==========")
    print(f"Total archivos: {len(file_list)}")
    print(f"Éxitos: {len(success_list)}")
    for f in success_list:
        print(f"   - {f}")
    print(f"Fallos: {len(fail_list)}")
    for f in fail_list:
        print(f"   - {f}")
    print("=============================")
