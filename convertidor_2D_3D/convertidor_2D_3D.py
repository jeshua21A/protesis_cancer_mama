import os
import subprocess
from PIL import Image
import shutil

# Rutas principales
input_folder = "imagenes_originales"
resized_folder = "imagenes_reescaladas"
output_folder = "modelo_salida"
database_path = os.path.join(output_folder, "colmap.db")
sparse_folder = os.path.join(output_folder, "sparse")
dense_folder = os.path.join(output_folder, "dense")
meshes_folder = os.path.join(dense_folder, "meshes")

# Paso 1: Redimensionar imágenes
def resize_images(max_size=2000):
    os.makedirs(resized_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            img.thumbnail((max_size, max_size))
            img.save(os.path.join(resized_folder, filename))

# Paso 2: Ejecutar comandos de COLMAP
def run_colmap():
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(sparse_folder, exist_ok=True)
    os.makedirs(dense_folder, exist_ok=True)

    def run_cmd(cmd):
        print(f"\n>> Ejecutando: {cmd}")
        subprocess.run(cmd, shell=True, check=True)

    # Feature Extraction
    run_cmd(f"colmap feature_extractor --database_path {database_path} "
            f"--image_path {resized_folder} --ImageReader.single_camera 1")

    # Feature Matching
    run_cmd(f"colmap exhaustive_matcher --database_path {database_path}")

    # Structure from Motion (Reconstrucción de cámara y nube de puntos)
    run_cmd(f"colmap mapper --database_path {database_path} --image_path {resized_folder} "
            f"--output_path {sparse_folder}")

    # Convertir modelo a formato binario para uso posterior
    run_cmd(f"colmap model_converter --input_path {os.path.join(sparse_folder, '0')} "
            f"--output_path {os.path.join(sparse_folder, '0')} --output_type TXT")

    # Densificación (Multi-view stereo)
    run_cmd(f"colmap image_undistorter --image_path {resized_folder} "
            f"--input_path {os.path.join(sparse_folder, '0')} "
            f"--output_path {dense_folder} --output_type COLMAP --max_image_size 2000")

    # Reconstrucción densa (Malla 3D)
    run_cmd(f"colmap patch_match_stereo --workspace_path {dense_folder} --workspace_format COLMAP --PatchMatchStereo.geom_consistency true")

    run_cmd(f"colmap stereo_fusion --workspace_path {dense_folder} --workspace_format COLMAP "
            f"--input_type geometric --output_path {os.path.join(dense_folder, 'fused.ply')}")

    # Reconstrucción de la malla (opcional)
    os.makedirs(meshes_folder, exist_ok=True)
    run_cmd(f"colmap poisson_mesher --input_path {os.path.join(dense_folder, 'fused.ply')} "
            f"--output_path {os.path.join(meshes_folder, 'mesh.ply')}")

# Ejecutar todo el flujo
if __name__ == "__main__":
    print("Redimensionando imágenes...")
    resize_images(max_size=2000)

    print("Ejecutando reconstrucción COLMAP...")
    run_colmap()

    print("\nProceso completado. Modelo 3D generado en:", output_folder)
