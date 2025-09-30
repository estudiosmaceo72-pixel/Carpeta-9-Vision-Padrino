import asyncio
from playwright.async_api import async_playwright
import time

IMAGEN = "imagenes/20250107_150516.jpg"
TEXTO = "Prueba de tiempos con Playwright ⏱️"

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

        # Medir tiempo: abrir Facebook
        t0 = time.time()
        await page.goto("https://www.facebook.com/")
        await page.wait_for_timeout(5000)
        print(f"✅ Facebook cargó en {time.time() - t0:.2f} segundos")

        # Intentar abrir cuadro de publicación (clic brutal con JS)
        try:
            await page.wait_for_timeout(5000)
            await page.evaluate("""
            () => {
                const botones = Array.from(document.querySelectorAll("div[role='button']"));
                const btn = botones.find(el => el.innerText && el.innerText.includes("¿Qué estás pensando"));
                if (btn) btn.click();
            }
            """)
            print("🟢 Clic forzado con JS en '¿Qué estás pensando?'")
        except:
            await page.wait_for_timeout(5000)
            await page.evaluate("""
            () => {
                const btn = document.querySelector("div[aria-label='Crear una publicación']");
                if (btn) btn.click();
            }
            """)
            print("🟢 Clic forzado con JS en 'Crear una publicación'")

        await page.wait_for_timeout(3000)

        # Medir tiempo: escribir texto
        t1 = time.time()
        await page.fill("div[role='textbox']", TEXTO)
        print(f"📝 Texto escrito en {time.time() - t1:.2f} segundos")

        # Medir tiempo: subir imagen
        t2 = time.time()
        input_file = await page.query_selector("input[type='file']")
        await input_file.set_input_files(IMAGEN)
        print(f"🖼️ Imagen cargada en {time.time() - t2:.2f} segundos")

        # Medir tiempo: botón "Siguiente"
        t3 = time.time()
        await page.wait_for_timeout(5000)  # esperar un poco antes de buscar
        await page.evaluate("""
        () => {
            const botones = Array.from(document.querySelectorAll("div[role='button'], span"));
            const btn = botones.find(el => el.innerText && el.innerText.includes("Siguiente"));
            if (btn) btn.click();
        }
        """)
        print(f"➡️ Botón 'Siguiente' clickeado en {time.time() - t3:.2f} segundos")

        # Medir tiempo: botón "Publicar"
        t4 = time.time()
        await page.wait_for_selector("div[role='button']:has-text('Publicar')", timeout=20000)
        print(f"📢 Botón 'Publicar' apareció en {time.time() - t4:.2f} segundos")

        # Medir tiempo: popup WhatsApp
        try:
            t5 = time.time()
            await page.wait_for_selector("div[role='button']:has-text('Ahora no')", timeout=5000)
            await page.click("div[role='button']:has-text('Ahora no')")
            print(f"❌ Popup WhatsApp cerrado en {time.time() - t5:.2f} segundos")
        except:
            print("✅ No apareció popup de WhatsApp")

        print(f"⏱️ Tiempo total del flujo: {time.time() - start_total:.2f} segundos")

        await page.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
