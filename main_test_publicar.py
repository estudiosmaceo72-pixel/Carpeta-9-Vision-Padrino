import asyncio
from playwright.async_api import async_playwright
import time

IMAGEN = "imagenes/20250107_150516.jpg"
TEXTO = "Publicación de prueba automática con Playwright 🚀 #ConstruyeConMaceo"

async def main():
    async with async_playwright() as p:
        print("⏳ Iniciando navegador...")
        start_total = time.time()

        browser = await p.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=False,
            args=["--start-maximized"]
        )
        page = await browser.new_page()

        # Abrir Facebook
        t0 = time.time()
        await page.goto("https://www.facebook.com/")
        await page.wait_for_timeout(5000)
        print(f"✅ Facebook cargó en {time.time() - t0:.2f} segundos")

        # Abrir cuadro de publicación con JS forzado
        await page.wait_for_timeout(5000)
        await page.evaluate("""
        () => {
            const botones = Array.from(document.querySelectorAll("div[role='button']"));
            const btn = botones.find(el => el.innerText && el.innerText.includes("¿Qué estás pensando"));
            if (btn) btn.click();
        }
        """)
        print("🟢 Clic en '¿Qué estás pensando?'")

        await page.wait_for_timeout(3000)

        # Escribir texto
        t1 = time.time()
        await page.fill("div[role='textbox']", TEXTO)
        print(f"📝 Texto escrito en {time.time() - t1:.2f} segundos")

        # Subir imagen
        t2 = time.time()
        input_file = await page.query_selector("input[type='file']")
        await input_file.set_input_files(IMAGEN)
        print(f"🖼️ Imagen cargada en {time.time() - t2:.2f} segundos")

        # Botón "Siguiente"
        await page.wait_for_timeout(5000)
        await page.evaluate("""
        () => {
            const botones = Array.from(document.querySelectorAll("div[role='button'], span"));
            const btn = botones.find(el => el.innerText && el.innerText.includes("Siguiente"));
            if (btn) btn.click();
        }
        """)
        print("➡️ Clic en 'Siguiente'")

        # Esperar que aparezca "Publicar"
        await page.wait_for_timeout(5000)

        # Cerrar popup de WhatsApp si aparece
        try:
            await page.wait_for_selector("div[role='button']:has-text('Ahora no')", timeout=5000)
            await page.click("div[role='button']:has-text('Ahora no')")
            print("❌ Popup WhatsApp cerrado")
        except:
            print("✅ No apareció popup de WhatsApp")

        # Botón "Publicar"
        t3 = time.time()
        await page.evaluate("""
        () => {
            const botones = Array.from(document.querySelectorAll("div[role='button'], span"));
            const btn = botones.find(el => el.innerText && el.innerText.includes("Publicar"));
            if (btn) btn.click();
        }
        """)
        print(f"📢 Clic en 'Publicar' ejecutado en {time.time() - t3:.2f} segundos")

        # Mantener navegador abierto para verificar
        print("⏳ Esperando 15 segundos para verificar publicación...")
        await page.wait_for_timeout(15000)

        print(f"✅ Flujo completo terminado en {time.time() - start_total:.2f} segundos")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
