import asyncio
from playwright.async_api import async_playwright

PAGE_URL = "https://www.facebook.com/Construyeconmaceo"
MENSAJE = "Probando publicación automática con el bot 🤖"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=120)
        context = await browser.new_context()
        page = await context.new_page()

        # Ir directo a la página
        await page.goto(PAGE_URL)
        print("🌐 Abriendo Construyeconmaceo...")

        # Esperar hasta que estemos en la página correcta
        await page.wait_for_url(PAGE_URL, timeout=300000)  # espera hasta 5 min
        await page.wait_for_load_state("networkidle")
        print("✅ Estamos dentro de Construyeconmaceo")

        # Intentar abrir el cuadro de publicación
        try:
            await page.locator("span:has-text('¿Qué estás pensando, Construyeconmaceo?')").click(timeout=20000)
            print("🖱️ Se hizo clic en el cuadro de publicación")

            # Escribir mensaje
            await page.locator("div[role='textbox']").fill(MENSAJE)
            print("✍️ Texto escrito en el cuadro de publicación")
        except Exception as e:
            print("⚠️ No pude interactuar con el cuadro:", e)

        # Mantener navegador abierto
        print("⏸️ Navegador abierto. Haz tus pruebas manuales si quieres.")
        await asyncio.sleep(999999)

asyncio.run(run())
