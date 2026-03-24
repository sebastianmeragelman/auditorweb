import cv2
import numpy as np
from PIL import Image
import os


# ==============================
# 🎞️ EXTRAER FRAMES DE UN GIF
# ==============================
def extract_frames_from_gif(gif_path, max_frames=3):
    frames = []
    try:
        gif = Image.open(gif_path)

        for i in range(max_frames):
            try:
                gif.seek(i)
                frame = np.array(gif.convert("RGB"))
                frames.append(frame)
            except EOFError:
                break

    except Exception as e:
        print(f"Error leyendo GIF {gif_path}: {e}")

    return frames


# ==============================
# 📂 CARGAR TODOS LOS BANNERS
# ==============================
def load_all_banner_frames(folder="banners"):
    banner_frames = []

    if not os.path.exists(folder):
        print(f"Carpeta de banners no existe: {folder}")
        return banner_frames

    for file in os.listdir(folder):
        if file.lower().endswith(".gif"):
            path = os.path.join(folder, file)
            print(f"Cargando banner: {file}")

            frames = extract_frames_from_gif(path)

            if not frames:
                print(f"No se pudieron extraer frames de {file}")
                continue

            banner_frames.extend(frames)

    print(f"Total frames cargados: {len(banner_frames)}")
    return banner_frames


# ==============================
# 🔍 DETECCIÓN DE BANNER (ROBUSTA + EDGES)
# ==============================
def find_banner_in_image(screenshot_path, banner_frames):

    screenshot = cv2.imread(screenshot_path)

    if screenshot is None:
        print("No se pudo leer screenshot")
        return False

    # 🎯 PREPROCESADO
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screen_blur = cv2.GaussianBlur(screen_gray, (5, 5), 0)

    # 👉 bordes del screenshot
    edges_screen = cv2.Canny(screen_gray, 50, 150)

    for idx, frame in enumerate(banner_frames):

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

        # 🔁 MULTI-SCALE
        scales = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

        for scale in scales:
            try:
                resized = cv2.resize(frame_blur, None, fx=scale, fy=scale)
            except:
                continue

            h, w = resized.shape[:2]

            # 🚨 evitar crash
            if h > screen_blur.shape[0] or w > screen_blur.shape[1]:
                continue

            # 🚫 evitar ruido (matches chicos)
            if w < 100 or h < 50:
                continue

            try:
                # ==============================
                # 🥇 MATCH 1 → similitud global
                # ==============================
                result1 = cv2.matchTemplate(
                    screen_blur,
                    resized,
                    cv2.TM_CCORR_NORMED
                )

                min_val, max_val1, min_loc, max_loc = cv2.minMaxLoc(result1)

                if max_val1 < 0.80:
                    continue

                # ==============================
                # 🥈 MATCH 2 → estructura
                # ==============================
                result2 = cv2.matchTemplate(
                    screen_blur,
                    resized,
                    cv2.TM_CCOEFF_NORMED
                )

                _, max_val2, _, _ = cv2.minMaxLoc(result2)

                if max_val2 < 0.70:
                    continue

                # ==============================
                # 🥉 MATCH 3 → bordes (CLAVE)
                # ==============================
                edges_template = cv2.Canny(resized, 50, 150)

                result3 = cv2.matchTemplate(
                    edges_screen,
                    edges_template,
                    cv2.TM_CCOEFF_NORMED
                )

                _, max_val3, _, _ = cv2.minMaxLoc(result3)

                print(
                    f"[Frame {idx} | Scale {scale}] → "
                    f"CCORR: {max_val1:.3f} | "
                    f"CCOEFF: {max_val2:.3f} | "
                    f"EDGES: {max_val3:.3f}"
                )

                # 🎯 VALIDACIÓN FINAL
                if max_val3 >= 0.50:
                    print("🎯 MATCH REAL VALIDADO")
                    return True

            except Exception as e:
                print(f"Error en matchTemplate: {e}")
                continue

    return False
