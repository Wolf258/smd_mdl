import bpy
import os 
import json
import sys

# Obtener la ruta relativa del script.
SCRIPT_material_obtainer_DIR = os.path.dirname(os.path.abspath(__file__))

# === Configuración ===
DEFAULT_INPUT = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/models/Christmas_Hat.fbx")

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Importa el FBX
fbx_path = os.path.abspath(DEFAULT_INPUT)
if not os.path.exists(fbx_path):
    raise FileNotFoundError(f"No se encontró el archivo FBX en {fbx_path}")

bpy.ops.import_scene.fbx(filepath=fbx_path)

# Diccionario para almacenar materiales y sus texturas
materials_dict = {}

for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    for slot in obj.material_slots:
        mat = slot.material
        if not mat:
            continue
        mat_name = mat.name
        textures = []
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    textures.append(os.path.basename(node.image.filepath))
        textures = list(dict.fromkeys(textures))
        materials_dict[mat_name] = textures

# Enviar el JSON directamente al manager
print("Materials:" + json.dumps(materials_dict))

# Guardamos a JSON
OUTPUT_JSON = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/models/materials.json")
with open(OUTPUT_JSON, "w") as f:
    json.dump(materials_dict, f, indent=4)
print(f"data: {OUTPUT_JSON}")
print(json.dumps(materials_dict, indent=4))