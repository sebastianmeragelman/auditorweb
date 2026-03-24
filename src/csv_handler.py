import csv
import os
from datetime import datetime


def read_urls(csv_path):
    urls = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            urls.append(row["url"])

    return urls


def append_result(csv_path, url, result, file_path):
    file_exists = os.path.exists(csv_path)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ["url", "fecha", "resultado", "archivo"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "url": url,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "resultado": result,
            "archivo": file_path
        })
