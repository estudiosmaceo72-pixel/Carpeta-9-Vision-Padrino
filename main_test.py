import asyncio
from playwright.async_api import async_playwright
import os

CARPETA_IMAGENES = "imagenes"

# Solo un producto de prueba
producto = {"archivo": "20250107_150516.jpg", "texto": "🧪 Prueba de publicación automática con foto 🚀"}

async def publicar_producto(page, producto):
    print(f"📢 Probando publicación con: {producto['archivo']}")

    # Ir a inicio de Facebook
    await page.goto("https://www.facebook.com/", wait_until="domcontentloaded")

    # Cerrar popup si aparece
    try:
        await page.get_by_text("Ahora no").click(timeout=5000)
    except:
        pass

    # Abrir cuadro de publicación
    await page.get_by_text("¿Qué estás pensando").first.click()
    await page.wait_for_timeout(3000)

    # Escribir texto
    await page.locator("div[role='textbox']").fill(producto["texto"])
    print("✍️ Texto escrito")
    await page.wait_for_timeout(5000)

    # Subir foto (forzado al input nativo)
    ruta_imagen = os.path.join(CARPETA_IMAGENES, producto["archivo"])
    await page.set_input_files("input[type='file']", ruta_imagen)
    print("📷 Imagen enviada al input")
    await page.wait_for_timeout(12000)

    # Intentar dar clic en Siguiente
    try:
        await page.get_by_role("button", name="Siguiente").click(timeout=10000)
        print("➡️ Clic en Siguiente")
        await page.wait_for_timeout(5000)
    except:
        print("⚠️ No apareció el botón Siguiente (puede ir directo a Publicar)")

    # Intentar dar clic en Publicar (más flexible)
    try:
        boton_publicar = page.get_by_role("button", name=lambda name: "Publicar" in name or "Post" in name)
        await boton_publicar.click(timeout=10000)
        print("✅ Clic en Publicar")
    except:
        print("❌ No se encontró el botón 'Publicar'")

    # Esperar un poco para observar
    await page.wait_for_timeout(20000)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            "userdata",
            headless=False,
            args=["--start-maximized"],
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )
        page = await browser.new_page()

        await publicar_producto(page, producto)

if __name__ == "__main__":
    asyncio.run(main())
