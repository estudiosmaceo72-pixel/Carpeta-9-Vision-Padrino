import asyncio
from playwright.async_api import async_playwright

PUBLICACION_TEXTO = "Hola comunidad 👷‍♂️🚀 Construyeconmaceo sigue creciendo. ¡Visítanos y comparte! 💪✨"

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=False
        )
        page = await browser.new_page()
        await page.goto("https://www.facebook.com", timeout=60000)

        # Cerrar popup de WhatsApp si aparece
        try:
            await page.wait_for_selector("text=Ahora no", timeout=5000)
            await page.click("text=Ahora no")
            print("Popup de WhatsApp cerrado")
        except:
            print("No apareció popup de WhatsApp")

        # Hacer clic en el cuadro "¿Qué estás pensando?"
        try:
            await page.wait_for_selector("div[role='button'] span:has-text('¿Qué estás pensando')", timeout=20000)
            await page.click("div[role='button'] span:has-text('¿Qué estás pensando')")
            print("✅ Se abrió el cuadro de publicación")
        except:
            print("❌ No se pudo abrir el cuadro de publicación")
            await browser.close()
            return

        # Buscar caja de texto
        caja_texto = None
        try:
            await page.wait_for_selector("div[role='textbox']", timeout=10000)
            caja_texto = await page.query_selector("div[role='textbox']")
            print("Se encontró caja de texto con role='textbox'")
        except:
            try:
                caja_texto = await page.get_by_role("textbox")
                print("Se encontró caja de texto con get_by_role")
            except:
                try:
                    caja_texto = await page.query_selector("div[aria-label*='¿Qué estás pensando']")
                    print("Se encontró caja de texto con aria-label")
                except:
                    pass

        # Escribir texto
        if caja_texto:
            await caja_texto.click()
            for char in PUBLICACION_TEXTO:
                await page.keyboard.type(char, delay=80)
            print("✅ Texto escrito correctamente")
        else:
            print("❌ No se encontró el cuadro de texto")

        # Hacer clic en "Siguiente"
        try:
            await page.wait_for_selector("div[aria-label='Siguiente']", timeout=15000)
            await page.click("div[aria-label='Siguiente']")
            print("✅ Se hizo clic en 'Siguiente'")
        except:
            print("❌ No se encontró el botón 'Siguiente'")

        # Hacer clic en "Publicar"
        try:
            await page.wait_for_selector("div[aria-label='Publicar']", timeout=20000)
            await page.click("div[aria-label='Publicar']")
            print("✅ Se hizo clic en 'Publicar'")
        except:
            print("❌ No se encontró el botón 'Publicar'")

        # Esperar para confirmar
        await asyncio.sleep(30)
        await browser.close()

asyncio.run(run_bot())
