import pyassimp
import numpy as np

def normalize_model(model_path, ref_path):
    """
    Calcula el factor de escala para normalizar el modelo basado en el eje Y (altura) del modelo de referencia.
    
    :param model_path: Ruta al modelo FBX a normalizar.
    :param ref_path: Ruta al modelo de referencia FBX.
    :return: Factor de escala (float) para aplicar uniformemente.
    """
    def get_height_y(scene):
        """Obtiene la altura en el eje Y (max_y - min_y) de la escena completa."""
        all_vertices = []
        for mesh in scene.meshes:
            all_vertices.extend(mesh.vertices)
        
        if not all_vertices:
            raise ValueError("No se encontraron vértices en la escena.")
        
        vertices_array = np.array(all_vertices)
        min_y = np.min(vertices_array[:, 1])  # Eje Y es el índice 1
        max_y = np.max(vertices_array[:, 1])
        height_y = max_y - min_y
        
        if height_y == 0:
            raise ValueError("La altura en Y es cero, no se puede calcular el factor.")
        
        return height_y
    
    # Cargar referencia
    ref_scene = pyassimp.load(ref_path)
    ref_height = get_height_y(ref_scene)
    pyassimp.release(ref_scene)
    
    # Cargar modelo
    model_scene = pyassimp.load(model_path)
    model_height = get_height_y(model_scene)
    pyassimp.release(model_scene)
    
    # Calcular factor
    scale_factor = ref_height / model_height
    print(f"[INFO] Factor de escala calculado para {model_path}: {scale_factor}")
    
    return scale_factor