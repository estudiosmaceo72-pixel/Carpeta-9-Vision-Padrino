import os
import shutil
import glob

# Ruta base del proyecto
BASE_DIR = r"C:\IMB_Digital\Bots\Bot_Publicador_Playwright"
ORIGEN_DIR = os.path.join(BASE_DIR, "Fotos_para_guardar")  # Carpeta temporal donde pondrás la foto
DESTINO_DIR = os.path.join(BASE_DIR, "GitGut_Archivos", "Fotos")

# Buscar el último número de versión guardado
def obtener_siguiente_version():
    archivos = [f for f in os.listdir(DESTINO_DIR) if f.startswith("Foto_") and f.endswith(".png")]
    numeros = []
    for archivo in archivos:
        try:
            num = int(archivo.replace("Foto_", "").replace(".png", ""))
            numeros.append(num)
        except:
            pass
    return max(numeros, default=0) + 1

def guardar_foto():
    # Buscar primera foto en la carpeta temporal
    fotos = glob.glob(os.path.join(ORIGEN_DIR, "*.png"))
    if not fotos:
        print("⚠️ No encontré ninguna foto en Fotos_para_guardar.")
        return
    
    origen = fotos[0]  # Tomar la primera foto encontrada
    siguiente = obtener_siguiente_version()
    nombre_destino = f"Foto_{siguiente:03d}.png"
    ruta_destino = os.path.join(DESTINO_DIR, nombre_destino)
    
    shutil.move(origen, ruta_destino)
    print(f"✅ Foto guardada: {nombre_destino}")

if __name__ == "__main__":
    guardar_foto()
