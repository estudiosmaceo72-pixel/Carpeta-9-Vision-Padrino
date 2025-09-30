import os
import shutil

# Ruta base del proyecto
BASE_DIR = r"C:\IMB_Digital\Bots\Bot_Publicador_Playwright"
ORIGEN = os.path.join(BASE_DIR, "bot_playwright.py")
DESTINO_DIR = os.path.join(BASE_DIR, "GitGut_Archivos", "Codigos")

# Buscar el último número de versión guardado
def obtener_siguiente_version():
    archivos = [f for f in os.listdir(DESTINO_DIR) if f.startswith("Codigo_") and f.endswith(".py")]
    numeros = []
    for archivo in archivos:
        try:
            num = int(archivo.replace("Codigo_", "").replace(".py", ""))
            numeros.append(num)
        except:
            pass
    return max(numeros, default=0) + 1

def guardar_version():
    if not os.path.exists(ORIGEN):
        print("⚠️ No se encontró bot_playwright.py en la ruta.")
        return
    
    siguiente = obtener_siguiente_version()
    nombre_destino = f"Codigo_{siguiente:03d}.py"
    ruta_destino = os.path.join(DESTINO_DIR, nombre_destino)
    
    shutil.copy2(ORIGEN, ruta_destino)
    print(f"✅ Versión guardada: {nombre_destino}")

if __name__ == "__main__":
    guardar_version()
