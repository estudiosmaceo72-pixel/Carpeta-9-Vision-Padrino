import asyncio
from playwright.async_api import async_playwright
import json
import os

async def main():
    # Cargar configuración
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    USER_DATA_DIR = "userdata"
    facebook_url = "https://www.facebook.com/"
    texto = config.get("texto", "Publicación automática de prueba 🚀")
    imagen_path = os.path.join("imagenes", config.get("imagen", "ejemplo.jpg"))

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"]
        )
        page = await browser.new_page()

        # 1. Abrir Facebook
        await page.goto(facebook_url, timeout=60000)
        await page.wait_for_timeout(8000)

        # 2. Cerrar popup de WhatsApp si aparece
        try:
            boton_ahora_no = page.locator("text=Ahora no")
            if await boton_ahora_no.is_visible():
                await boton_ahora_no.click()
        except:
            pass

        # 3. Abrir el cuadro de publicación
        await page.click("div[role='button']:has-text('¿Qué estás pensando')")
        await page.wait_for_timeout(3000)

        # 4. Escribir el texto
        editor = page.locator("div[role='textbox']")
        await editor.click()
        await editor.fill("")  # limpiar primero
        await page.keyboard.type(texto, delay=80)

        # 5. Subir imagen
        input_file = page.locator("input[type='file']")
        await input_file.set_input_files(imagen_path)
        await page.wait_for_timeout(5000)

        # 6. Clic en Siguiente
        try:
            boton_siguiente = page.locator("div[role='button']:has-text('Siguiente')")
            await boton_siguiente.wait_for(state="visible", timeout=10000)
            await boton_siguiente.click()
        except:
            print("⚠️ No encontré el botón Siguiente")

        await page.wait_for_timeout(3000)

        # 7. Clic en Publicar
        try:
            boton_publicar = page.locator("div[role='button']:has-text('Publicar')")
            await boton_publicar.wait_for(state="visible", timeout=10000)
            await boton_publicar.click()
            print("✅ Publicación enviada")
        except:
            print("⚠️ No encontré el botón Publicar")

        # Esperar un rato para confirmar
        await page.wait_for_timeout(10000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
