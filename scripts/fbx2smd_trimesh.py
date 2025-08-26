import trimesh
import os
import sys
import numpy as np

def export_smd(mesh, output_path, material_name="default_material"):
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

        # Obtener vértices, normales y coordenadas UV
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Calcular normales si no existen
        if hasattr(mesh, 'face_normals') and mesh.face_normals is not None:
            face_normals = mesh.face_normals
        else:
            face_normals = mesh.face_normals
        
        # Obtener coordenadas UV si existen
        if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'uv'):
            uvs = mesh.visual.uv
        else:
            uvs = None

        for i, face in enumerate(faces):
            f.write(f"{material_name}\n")
            
            # Para cada vértice en la cara
            for j, vertex_idx in enumerate(face):
                v = vertices[vertex_idx]
                
                # Normal del vértice (usar normal de la cara si no hay normales de vértice)
                if hasattr(mesh, 'vertex_normals') and mesh.vertex_normals is not None:
                    n = mesh.vertex_normals[vertex_idx]
                else:
                    n = face_normals[i] if face_normals is not None else [0.0, 0.0, 1.0]
                
                # Coordenadas UV
                if uvs is not None and vertex_idx < len(uvs):
                    uv = uvs[vertex_idx][:2]
                else:
                    uv = [0.0, 0.0]

                # Formato vértice: boneID pos.x pos.y pos.z norm.x norm.y norm.z uv.x uv.y
                f.write(f" 0 {v[0]:.6f} {v[1]:.6f} {v[2]:.6f} {n[0]:.6f} {n[1]:.6f} {n[2]:.6f} {uv[0]:.6f} {uv[1]:.6f}\n")

        f.write("end\n")


def convert_to_smd(input_path, output_path):
    print(f"[INFO] Cargando modelo: {input_path}")
    
    try:
        # Cargar el modelo con trimesh
        mesh = trimesh.load(input_path)
        
        # Si es una escena con múltiples mallas, combinar en una sola
        if isinstance(mesh, trimesh.Scene):
            print(f"[INFO] Escena detectada con {len(mesh.geometry)} objetos.")
            # Combinar todas las mallas en una sola
            meshes = list(mesh.geometry.values())
            if meshes:
                combined_mesh = trimesh.util.concatenate(meshes)
                print(f"[INFO] Combinando {len(meshes)} mallas en una sola.")
            else:
                print("[ERROR] No se encontraron mallas en la escena.")
                return
        else:
            combined_mesh = mesh
            print(f"[INFO] Malla única cargada con {len(combined_mesh.vertices)} vértices.")
        
        export_smd(combined_mesh, output_path)
        print(f"[OK] Exportado a SMD: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Error al cargar el modelo: {e}")
        return


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python fbx2smd_trimesh.py input.fbx output.smd")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"[ERROR] No existe el archivo {input_path}")
        sys.exit(1)

    convert_to_smd(input_path, output_path)
