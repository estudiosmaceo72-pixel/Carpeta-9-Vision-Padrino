import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=False,
            args=["--start-maximized"]
        )
        page = await browser.new_page()

        print("Abriendo Facebook...")
        await page.goto("https://www.facebook.com", timeout=60000)

        # Esperar que cargue el área de publicar
        await page.wait_for_selector("div[role='button'][aria-label*='pensando']", timeout=60000)
        await page.click("div[role='button'][aria-label*='pensando']")

        # Escribir texto en el cuadro de publicación
        print("Escribiendo texto...")
        await page.wait_for_selector("div[role='textbox']", timeout=30000)
        await page.fill("div[role='textbox']", "🚀 Publicación automática con imagen y texto ✅")

        # Adjuntar imagen
        print("Cargando imagen...")
        await page.set_input_files("input[type='file']", "imagenes/producto1.jpg")

        # Manejar popup de WhatsApp si aparece
        try:
            await page.wait_for_selector("div[role='dialog'] div:has-text('Ahora no')", timeout=10000)
            await page.click("div[role='dialog'] div:has-text('Ahora no')")
            print("Popup de WhatsApp cerrado.")
        except:
            print("No apareció popup de WhatsApp.")

        # Clic en botón Siguiente
        print("Buscando botón 'Siguiente'...")
        await page.wait_for_selector("div[role='button']:has-text('Siguiente')", timeout=30000)
        await page.click("div[role='button']:has-text('Siguiente')")
        await page.wait_for_timeout(3000)

        # Clic en botón Publicar
        print("Publicando...")
        await page.wait_for_selector("div[role='button']:has-text('Publicar')", timeout=30000)
        await page.click("div[role='button']:has-text('Publicar')")

        # Esperar un momento para confirmar publicación
        await page.wait_for_timeout(60000)
        await browser.close()

asyncio.run(run_bot())
