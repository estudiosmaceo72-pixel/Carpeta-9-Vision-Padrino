from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)  # visible y más lento
    page = browser.new_page()
    page.goto("https://example.com")
    print("Título de la página:", page.title())
    input("Presiona Enter para cerrar...")
    browser.close()
