const { chromium } = require("playwright");
const fs = require("fs");

// Cargar config.json
const config = JSON.parse(fs.readFileSync("config.json", "utf8"));
const productos = config.productos;

// Carpeta donde guardamos las imágenes
const carpetaImagenes = "./imagenes/";

async function publicarProducto(page, producto) {
  console.log(`📢 Publicando: ${producto.archivo}`);

  // Ir al inicio de Facebook
  await page.goto("https://www.facebook.com/", { waitUntil: "domcontentloaded" });

  // Cerrar popup de WhatsApp si aparece
  try {
    await page.locator("text=Ahora no").click({ timeout: 5000 });
    console.log("🔒 Popup WhatsApp cerrado.");
  } catch {}

  // Hacer clic en el área de publicación
  await page.getByText("¿Qué estás pensando").first().click();

  // Escribir el texto del producto
  await page.keyboard.type(producto.texto, { delay: 50 });

  // Clic en "Agregar a tu publicación" → "Foto/video"
  await page.getByLabel("Foto/video").click();

  // Subir archivo de imagen
  const [fileChooser] = await Promise.all([
    page.waitForEvent("filechooser"),
    page.getByLabel("Agregar fotos o videos").click()
  ]);
  await fileChooser.setFiles(carpetaImagenes + producto.archivo);

  // Esperar a que cargue la imagen
  await page.waitForTimeout(5000);

  // Botón Siguiente
  try {
    await page.getByRole("button", { name: "Siguiente" }).click({ timeout: 10000 });
  } catch {
    console.log("⚠️ Botón 'Siguiente' no encontrado, intentando continuar...");
  }

  // Botón Publicar
  await page.getByRole("button", { name: "Publicar" }).click();

  console.log(`✅ Publicado: ${producto.archivo}`);

  // Esperar confirmación y revisión
  await page.waitForTimeout(60000); // 1 min revisión
}

async function main() {
  const browser = await chromium.launchPersistentContext("userdata", {
    headless: false,
    args: ["--start-maximized"],
  });

  const page = await browser.newPage();

  while (true) {
    for (const producto of productos) {
      try {
        await publicarProducto(page, producto);
      } catch (error) {
        console.error("❌ Error publicando:", error);
      }

      console.log("⏳ Esperando 2 minutos antes del siguiente...");
      await page.waitForTimeout(120000); // 2 minutos entre publicaciones
    }
  }
}

main();
