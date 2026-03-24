from playwright.sync_api import sync_playwright
import time
import os


def capture_screenshot(url, output_path):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )

            page = context.new_page()

            print(f"Abriendo URL: {url}")

            # 🚀 Ir a la página
            page.goto(url, timeout=60000)

            # Esperar DOM listo (más confiable que networkidle solo)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # Scroll progresivo (para cargar ads lazy)
            for _ in range(8):
                page.mouse.wheel(0, 800)
                time.sleep(1)

            # Espera extra
            time.sleep(3)

            # 📸 Screenshot
            page.screenshot(path=output_path, full_page=True)

            browser.close()

        # ✅ VALIDACIÓN CLAVE
        if not os.path.exists(output_path):
            return "ERROR: screenshot no guardado"

        if os.path.getsize(output_path) == 0:
            return "ERROR: screenshot vacío"

        print(f"Screenshot OK: {output_path}")
        return "OK"

    except Exception as e:
        print(f"Error captura: {e}")
        return f"ERROR: {str(e)}"
