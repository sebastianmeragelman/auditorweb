import os
import shutil
from playwright.sync_api import sync_playwright
import imghdr
import cv2


TEMP_FOLDER = "temp_banners"


# ==============================
# 🧹 LIMPIEZA
# ==============================
def cleanup_temp():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)


# ==============================
# 🌐 CAPTURA DE IMÁGENES
# ==============================
def capture_image_requests(url):

    os.makedirs(TEMP_FOLDER, exist_ok=True)
    downloaded_paths = []

    def handle_response(response):
        try:
            content_type = response.headers.get("content-type", "").lower()

            # 🔥 filtro clave
            if "image" not in content_type:
                return

            body = response.body()

            if not body or len(body) < 5000:
                return

            # 🔍 detectar tipo real
            ext_detected = imghdr.what(None, h=body)

            if ext_detected:
                ext = f".{ext_detected}"
            else:
                if "gif" in content_type:
                    ext = ".gif"
                elif "jpeg" in content_type or "jpg" in content_type:
                    ext = ".jpg"
                elif "png" in content_type:
                    ext = ".png"
                elif "webp" in content_type:
                    ext = ".webp"
                else:
                    ext = ".img"

            filename = os.path.join(
                TEMP_FOLDER,
                f"img_{len(downloaded_paths)}{ext}"
            )

            with open(filename, "wb") as f:
                f.write(body)

            downloaded_paths.append(filename)

            print(f"⬇ {filename} ({content_type})")

        except Exception as e:
            print(f"Error capturando imagen: {e}")

    # ==============================
    # ▶ PLAYWRIGHT
    # ==============================
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.on("response", handle_response)

            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)

            browser.close()

    except Exception as e:
        print(f"⚠️ Error en Playwright: {e}")

    return downloaded_paths


# ==============================
# 🧠 MATCH
# ==============================
def match_downloaded_vs_reference(downloaded_paths, banner_frames, threshold=0.75):

    if not downloaded_paths:
        return False

    # 🔥 priorización
    gif_paths = [p for p in downloaded_paths if p.endswith(".gif")]
    other_paths = [p for p in downloaded_paths if not p.endswith(".gif")]

    ordered_paths = gif_paths + other_paths

    print(f"🎞 GIFs: {len(gif_paths)} | Otras: {len(other_paths)}")

    for path in ordered_paths:

        img = cv2.imread(path)

        if img is None:
            continue

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for idx, frame in enumerate(banner_frames):

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            if frame_gray.shape[0] > img_gray.shape[0] or frame_gray.shape[1] > img_gray.shape[1]:
                continue

            result = cv2.matchTemplate(
                img_gray,
                frame_gray,
                cv2.TM_CCORR_NORMED
            )

            _, max_val, _, _ = cv2.minMaxLoc(result)

            print(f"{path} vs frame {idx} → {max_val:.3f}")

            if max_val >= threshold:
                print(f"🎯 MATCH: {max_val:.3f} en {path}")
                return True

    return False
