import asyncio
from playwright.async_api import async_playwright
import os

PUBLICACION_TEXTO = "Hola comunidad 👷‍♂️🚀 Construyeconmaceo sigue creciendo. ¡Visítanos y comparte! 💪✨"
CARPETA_IMAGENES = "imagenes"

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=False
        )
        page = await browser.new_page()
        await page.goto("https://www.facebook.com", timeout=60000)

        # Abrir cuadro de publicación
        try:
            await page.wait_for_selector("div[role='button'] span:has-text('¿Qué estás pensando')", timeout=20000)
            await page.click("div[role='button'] span:has-text('¿Qué estás pensando')")
            print("✅ Se abrió el cuadro de publicación")
        except:
            print("❌ No se pudo abrir el cuadro de publicación")
            await browser.close()
            return

        # Escribir texto
        try:
            await page.wait_for_selector("div[role='textbox']", timeout=10000)
            caja_texto = await page.query_selector("div[role='textbox']")
            await caja_texto.click()
            for char in PUBLICACION_TEXTO:
                await page.keyboard.type(char, delay=80)
            print("✅ Texto escrito correctamente")
        except:
            print("❌ No se encontró el cuadro de texto")

        # Adjuntar imagen
        try:
            archivos = os.listdir(CARPETA_IMAGENES)
            if archivos:
                ruta_imagen = os.path.join(CARPETA_IMAGENES, archivos[0])
                input_file = await page.query_selector("input[type='file']")
                await input_file.set_input_files(ruta_imagen)
                print(f"✅ Imagen adjuntada: {archivos[0]}")
        except Exception as e:
            print(f"❌ Error al adjuntar imagen: {e}")

        # Clic en "Siguiente"
        try:
            await page.wait_for_selector("div[aria-label='Siguiente']", timeout=20000)
            await page.click("div[aria-label='Siguiente']")
            print("✅ Se hizo clic en 'Siguiente'")
        except:
            print("❌ No se encontró el botón 'Siguiente'")

        # Manejo popup WhatsApp
        try:
            await page.wait_for_selector("text=Ahora no", timeout=7000)
            await page.click("text=Ahora no")
            print("✅ Popup de WhatsApp cerrado")
        except:
            print("No apareció popup de WhatsApp")

        # Clic en "Publicar" (intentando varios selectores)
        try:
            try:
                await page.wait_for_selector("div[aria-label='Publicar']", timeout=10000)
                await page.click("div[aria-label='Publicar']")
                print("✅ Publicación realizada con selector aria-label")
            except:
                await page.wait_for_selector("div[role='button']:has-text('Publicar')", timeout=10000)
                await page.click("div[role='button']:has-text('Publicar')")
                print("✅ Publicación realizada con selector por texto")
        except:
            print("❌ No se pudo hacer clic en 'Publicar'")

        await asyncio.sleep(20)
        await browser.close()

asyncio.run(run_bot())
