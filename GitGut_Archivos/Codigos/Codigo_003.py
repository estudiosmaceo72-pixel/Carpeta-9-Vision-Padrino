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

        # Abrir cuadro de publicación
        try:
            await page.wait_for_selector("div[role='button'][tabindex='0']", timeout=20000)
            botones = await page.query_selector_all("div[role='button'][tabindex='0']")
            if botones:
                await botones[0].click()
                print("Se abrió el cuadro de publicación")
        except:
            print("No se pudo abrir el cuadro de publicación")
            await browser.close()
            return

        # Intentar localizar el área de texto con varias estrategias
        caja_texto = None
        try:
            # Estrategia 1: selector directo
            await page.wait_for_selector("div[role='textbox']", timeout=10000)
            caja_texto = await page.query_selector("div[role='textbox']")
            print("Se encontró caja de texto con role='textbox'")
        except:
            print("No funcionó role='textbox'")

        if not caja_texto:
            try:
                # Estrategia 2: usando get_by_role
                caja_texto = await page.get_by_role("textbox")
                print("Se encontró caja de texto con get_by_role")
            except:
                print("No funcionó get_by_role")

        if not caja_texto:
            try:
                # Estrategia 3: buscar placeholder del mensaje
                caja_texto = await page.query_selector("div[aria-label*='¿Qué estás pensando']")
                print("Se encontró caja de texto con aria-label")
            except:
                print("No funcionó aria-label")

        # Escribir texto si se encontró el área editable
        if caja_texto:
            await caja_texto.click()
            for char in PUBLICACION_TEXTO:
                await page.keyboard.type(char, delay=80)
            print("✅ Texto escrito correctamente")
        else:
            print("❌ No se encontró el cuadro de texto")

        await asyncio.sleep(20)
        await browser.close()

asyncio.run(run_bot())
