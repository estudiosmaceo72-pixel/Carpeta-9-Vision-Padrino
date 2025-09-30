import asyncio
from playwright.async_api import async_playwright
import os

# Configuración
USER_DATA_DIR = r"C:\IMB_Digital\Bots\Bot_Publicador_Playwright\userdata"
IMAGEN = r"C:\IMB_Digital\Bots\Bot_Publicador_Playwright\imagenes\20251007.jpg"
TEXTO = "🚀 Publicación automática con Playwright ✅"

async def main():
    async with async_playwright() as p:
        # Abrir navegador con perfil persistente
        browser = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
        )
        page = await browser.new_page()

        print("🌐 Abriendo Facebook...")
        await page.goto("https://www.facebook.com/")

        # Abrir el cuadro de publicación
        print("📝 Buscando cuadro de publicación...")
        await page.wait_for_selector("div[role='button']:has-text('¿Qué estás pensando')", timeout=20000)
        await page.click("div[role='button']:has-text('¿Qué estás pensando')")

        # Escribir el texto
        print("⌨️ Escribiendo texto...")
        await page.wait_for_selector("div[role='textbox']", timeout=20000)
        await page.fill("div[role='textbox']", TEXTO)

        # Abrir opción "Foto/video"
        print("📷 Abriendo opción 'Foto/video'...")
        try:
            await page.wait_for_selector("div[role='button']:has-text('Foto/video')", timeout=15000)
            await page.click("div[role='button']:has-text('Foto/video')")
        except:
            print("⚠️ No se encontró el botón 'Foto/video'")

        # Subir la imagen
        print("🖼️ Subiendo imagen...")
        try:
            await page.set_input_files("input[type='file'][accept*='image']", IMAGEN)
            print("✅ Imagen cargada correctamente.")
        except Exception as e:
            print("❌ Error al cargar la imagen:", e)

        # Clic en "Siguiente"
        print("➡️ Buscando botón 'Siguiente'...")
        try:
            await page.wait_for_selector("div[role='button']:has-text('Siguiente')", timeout=20000)
            await page.click("div[role='button']:has-text('Siguiente')")
            print("✅ Se hizo clic en 'Siguiente'")
        except:
            print("❌ No se encontró botón 'Siguiente'")

        # Manejar popup de WhatsApp -> "Ahora no"
        print("📵 Revisando popup de WhatsApp...")
        try:
            await page.wait_for_selector("div[role='button']:has-text('Ahora no')", timeout=10000)
            await page.click("div[role='button']:has-text('Ahora no')")
            print("✅ Se cerró el popup de WhatsApp")
        except:
            print("✅ No apareció popup de WhatsApp")

        # Clic en "Publicar"
        print("📢 Buscando botón 'Publicar'...")
        try:
            await page.wait_for_selector("div[role='button']:has-text('Publicar')", timeout=20000)
            await page.click("div[role='button']:has-text('Publicar')")
            print("✅ Publicación enviada.")
        except:
            print("❌ No se encontró el botón 'Publicar'")

        # Esperar un poco para confirmar
        await page.wait_for_timeout(10000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
