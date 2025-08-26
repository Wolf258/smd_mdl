import pyassimp
import os
import sys
from os.path import join
from dotenv import load_dotenv

# Obtener la ruta relativa del script.
SCRIPT_fbx2smd_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar las variables de entorno del .env
load_dotenv(join(SCRIPT_fbx2smd_DIR, '../.env'))

# Obtener el path de los modelos/fbx. 
path_models_fbx = os.getenv('path_models_fbx')












def export_smd(scene, output_path, material_name="default_material"):
    with open(output_path, "w") as f:
        # Encabezado
        f.write("version 1\n")
        
        # Nodos (un hueso root para todo)
        f.write("nodes\n")
        f.write(" 0 \"root\" -1\n")
        f.write("end\n")

        # Esqueleto
        f.write("skeleton\n")
        f.write(" time 0\n")
        f.write(" 0 0.0 0.0 0.0 0 0 0\n")
        f.write("end\n")

        # Triángulos
        f.write("triangles\n")

        for mesh in scene.meshes:
            mat = material_name
            if scene.materials and mesh.materialindex < len(scene.materials):
                mat = scene.materials[mesh.materialindex].properties.get("name", material_name)

            for face in mesh.faces:
                if len(face) != 3:
                    continue  # solo triángulos

                f.write(f"{mat}\n")
                for idx in face:
                    v = mesh.vertices[idx]
                    n = mesh.normals[idx] if mesh.normals.any() else [0.0, 0.0, 1.0]
                    uv = [0.0, 0.0]
                    if mesh.texturecoords is not None and len(mesh.texturecoords) > 0:
                        uv = mesh.texturecoords[0][idx][:2]

                    # Formato vértice: boneID pos.x pos.y pos.z norm.x norm.y norm.z uv.x uv.y
                    f.write(f" 0 {v[0]} {v[1]} {v[2]} {n[0]} {n[1]} {n[2]} {uv[0]} {uv[1]}\n")

        f.write("end\n")


def convert_to_smd(input_path, output_path):
    print(f"[INFO] Cargando modelo: {input_path}")
    scene = pyassimp.load(input_path)

    print(f"[INFO] {len(scene.meshes)} mallas encontradas.")
    export_smd(scene, output_path)
    pyassimp.release(scene)

    print(f"[OK] Exportado a SMD: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python fbx2smd.py input.fbx output.smd")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"[ERROR] No existe el archivo {input_path}")
        sys.exit(1)

    convert_to_smd(input_path, output_path)
