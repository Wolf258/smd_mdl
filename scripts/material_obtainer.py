import bpy
import os 
import json
import sys

# === Configuración ===
SCRIPT_material_obtainer_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_list = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/temp/file_list.json")
DEFAULT_INPUT = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/models/")
TEMP_OUTPUT = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/temp/")

# Leer lista de archivos desde JSON_list
if not os.path.exists(JSON_list):
    raise FileNotFoundError(f"No se encontró la lista de archivos JSON en {JSON_list}")

with open(JSON_list, "r") as f:
    try:
        file_list = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"El archivo {JSON_list} no contiene un JSON válido")

if not isinstance(file_list, list):
    raise ValueError(f"El archivo {JSON_list} debe contener una lista de nombres de archivos FBX")

# Diccionario global con todos los materiales
all_materials = {}

# Procesar cada FBX en la lista
for filename in file_list:
    fbx_path = os.path.join(DEFAULT_INPUT, filename)
    if not os.path.exists(fbx_path):
        print(f"⚠️ No se encontró el archivo: {fbx_path}")
        continue

    # Limpia la escena antes de importar cada archivo
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Importar el FBX
    bpy.ops.import_scene.fbx(filepath=fbx_path)

    # Diccionario de materiales de este archivo
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
            # eliminar duplicados conservando orden
            textures = list(dict.fromkeys(textures))
            materials_dict[mat_name] = textures

    # Añadir al diccionario global bajo el nombre del archivo
    all_materials[filename] = materials_dict

# Enviar todo el JSON combinado al manager (stdout)
print("Materials:" + json.dumps(all_materials))

# Guardar también un JSON global en resources/temp
OUTPUT_JSON = os.path.join(SCRIPT_material_obtainer_DIR, "../resources/temp/materials.json")
with open(OUTPUT_JSON, "w") as f:
    json.dump(all_materials, f, indent=4)

print(f"data: {OUTPUT_JSON}")
print(json.dumps(all_materials, indent=4))
