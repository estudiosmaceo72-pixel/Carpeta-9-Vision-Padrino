import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    # Usamos perfil persistente para evitar logins repetidos
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir="userdata",
        headless=False,
        args=["--start-maximized"]
    )

    # Abrir una nueva pestaña
    page = await browser.new_page()

    # Ir directo a la página de inicio de Facebook
    await page.goto("https://www.facebook.com/")
    await page.wait_for_load_state("networkidle")

    print("✅ Página de inicio de Facebook abierta.")

    try:
        # Abrir cuadro de publicación
        print("📝 Abriendo cuadro de publicación...")
        await page.get_by_text("¿Qué estás pensando, Construyeconmaceo?", exact=False).click()
        await page.wait_for_selector("div[role='textbox']", timeout=20000)

        # Escribir texto
        await page.fill("div[role='textbox']", "🚀 Publicación automática de prueba con Playwright")
        print("✍️ Texto escrito.")

        # Clic en "Siguiente"
        print("👉 Haciendo clic en 'Siguiente'...")
        await page.get_by_role("button", name="Siguiente").click()

        # Esperar y hacer clic en el botón azul "Publicar"
        print("👉 Buscando botón azul 'Publicar'...")
        await page.wait_for_selector("div[role='button']:has-text('Publicar'), button:has-text('Publicar')", timeout=20000)

        publicar_buttons = page.locator("div[role='button']:has-text('Publicar'), button:has-text('Publicar')")
        count = await publicar_buttons.count()
        if count > 0:
            await publicar_buttons.nth(count - 1).click()
            print("✅ Publicación realizada con éxito.")
        else:
            print("❌ No se encontró el botón 'Publicar'.")

        # Detectar popup de WhatsApp y cerrarlo
        try:
            print("👉 Revisando si aparece popup de WhatsApp...")
            await page.wait_for_selector("div[role='button']:has-text('Ahora no')", timeout=5000)
            await page.locator("div[role='button']:has-text('Ahora no')").click()
            print("✅ Popup de WhatsApp cerrado.")
        except:
            print("ℹ️ No apareció popup de WhatsApp.")
    except Exception as e:
        print("❌ Hubo un error en el proceso:", e)

    print("⌛ El bot quedará abierto hasta que cierres con CTRL+C en la consola.")
    await asyncio.Event().wait()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == "__main__":
    asyncio.run(main())
