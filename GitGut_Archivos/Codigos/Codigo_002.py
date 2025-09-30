import asyncio
from playwright.async_api import async_playwright

# Texto que publicaremos (puedes cambiarlo o leerlo de config.json más adelante)
PUBLICACION_TEXTO = "Hola comunidad 👷‍♂️🚀 Construyeconmaceo sigue creciendo. ¡Visítanos y comparte! 💪✨"

async def run_bot():
    async with async_playwright() as p:
        # Usamos perfil persistente para no tener que loguear cada vez
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=False
        )
        page = await browser.new_page()

        # Abrir Facebook
        await page.goto("https://www.facebook.com", timeout=60000)

        # Manejar posible popup de WhatsApp (botón "Ahora no")
        try:
            await page.wait_for_selector("text=Ahora no", timeout=5000)
            await page.click("text=Ahora no")
            print("Popup de WhatsApp cerrado con 'Ahora no'")
        except:
            print("No apareció popup de WhatsApp")

        # Abrir cuadro de publicación "¿Qué estás pensando, Construyeconmaceo?"
        await page.wait_for_selector("div[role='button'][tabindex='0']", timeout=15000)
        botones = await page.query_selector_all("div[role='button'][tabindex='0']")
        if botones:
            await botones[0].click()
            print("Se abrió el cuadro de publicación")

        # Esperar a que aparezca el área editable
        await page.wait_for_selector("div[role='textbox']", timeout=15000)
        caja_texto = await page.query_selector("div[role='textbox']")

        # Escribir texto poco a poco (para que parezca humano)
        await caja_texto.click()
        for char in PUBLICACION_TEXTO:
            await page.keyboard.type(char, delay=80)  # 80 ms entre teclas
        print("Texto escrito correctamente en la publicación")

        # --- Próximos pasos ---
        # Instrucción 2: aquí vendrá clic en "Siguiente"
        # Instrucción 3: clic en "Publicar"

        # Mantener navegador abierto un rato para verificar manualmente
        await asyncio.sleep(20)

        # Cerrar navegador
        await browser.close()

asyncio.run(run_bot())
