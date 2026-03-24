from src.browser import capture_screenshot
from src.banner_detector import load_all_banner_frames
from src.banner_scraper import (
    capture_image_requests,
    match_downloaded_vs_reference,
    cleanup_temp
)
from src.csv_handler import read_urls, append_result
from src.utils import sanitize_name, generate_filename, normalize_url

import os


INPUT_CSV = "input/urls.csv"
OUTPUT_CSV = "output/resultados.csv"


def main():
    print("🚀 INICIO PROCESO")

    urls = read_urls(INPUT_CSV)
    print(f"Cantidad de URLs: {len(urls)}")

    print("\n📦 Cargando banners...")
    banner_frames = load_all_banner_frames("banners")

    if not banner_frames:
        print("❌ ERROR: No hay banners cargados")
        return

    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    for i, url in enumerate(urls, start=1):

        if not url:
            continue

        try:
            url = normalize_url(url)

            print("\n" + "=" * 60)
            print(f"🌐 Procesando {i}: {url}")

            # ==============================
            # 📸 SIEMPRE SACAR SCREENSHOT
            # ==============================
            filename = f"{sanitize_name(url)}_{generate_filename()}.png"
            screenshot_path = f"data/{filename}"

            print("📸 Capturando screenshot...")
            capture_result = capture_screenshot(url, screenshot_path)

            if capture_result != "OK":
                print("⚠️ Error capturando screenshot")

            # ==============================
            # 🔎 CAPTURA DE IMÁGENES (network)
            # ==============================
            downloaded = capture_image_requests(url)

            print(f"📊 Imágenes capturadas: {len(downloaded)}")

            # ==============================
            # 🧠 MATCH
            # ==============================
            banner_found = False

            if downloaded:
                banner_found = match_downloaded_vs_reference(downloaded, banner_frames)
            else:
                print("⚠️ No hay imágenes para analizar")

            cleanup_temp()

            # ==============================
            # 🎯 RESULTADO FINAL
            # ==============================
            if banner_found:
                result = "BANNER OK"
                print("🎯 Banner detectado")
            else:
                result = "NO BANNER"
                print("❌ No se encontró banner")

            # ==============================
            # 💾 GUARDAR CSV
            # ==============================
            append_result(OUTPUT_CSV, url, result, screenshot_path)

        except Exception as e:
            print(f"❌ Error en {url}: {e}")
            append_result(OUTPUT_CSV, url, f"ERROR: {str(e)}", "")


if __name__ == "__main__":
    main()
