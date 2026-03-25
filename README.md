# auditorweb
Automated web banner auditing system that detects the presence of advertising banners on websites using network-level image extraction (Playwright) and visual similarity matching (OpenCV). Includes GIF support, screenshot evidence, and CSV reporting.

# 🕵️ Auditoría de Banners Web

Sistema automatizado para detectar la presencia de banners publicitarios en sitios web mediante:

- Captura de requests de imágenes (Playwright)
- Comparación por template matching (OpenCV)
- Soporte para banners GIF (multi-frame)

---

## 🚀 Features

- Detección de banners por comparación visual
- Captura automática de screenshots
- Scraping de imágenes vía network
- Priorización de GIFs
- Exportación de resultados a CSV


---
## ESTRUCTURA

src/ # lógica principal
banners/ # banners de referencia
input/ # URLs a auditar
output/ # resultados CSV
data/ # screenshots


---

## ⚙️ Instalación

```bash
git clone https://github.com/sebastianmeragelman/auditorweb.git
cd auditoria-banners/auditoriaweb

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
playwright install



python -m src.main
📊 Output

Archivo CSV con:

URL
Resultado (BANNER OK / NO BANNER)
Screenshot de respaldo
🧠 Tecnologías
Python
OpenCV
Playwright
PIL
