from flask import Flask, render_template, request, send_file, redirect, url_for
from bs4 import BeautifulSoup
import requests, csv, os
from urllib.parse import urlparse

app = Flask(__name__, template_folder='assets/template', static_folder='assets')

DATA_CSV = "scraped_data.csv"

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        items = []

        for tag in ["h1", "h2", "h3", "p", "li", "td", "th"]:
            for el in soup.find_all(tag):
                text = el.get_text(strip=True)
                if text:
                    items.append({"type": tag.upper(), "content": text})

        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                full_src = src if src.startswith("http") else url + "/" + src.lstrip("/")
                items.append({"type": "IMAGE", "content": full_src})

        return items
    except Exception as e:
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    data, error, url = [], "", ""
    if request.method == "POST":
        url = request.form.get("website_url", "").strip()
        if not is_valid_url(url):
            error = "❗ Please enter a valid URL (e.g., https://example.com)"
        else:
            data = scrape_website(url)
            if not data:
                error = "⚠️ No content could be extracted from this URL."
            else:
                with open(DATA_CSV, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["type", "content"])
                    writer.writeheader()
                    writer.writerows(data)
    return render_template("index.html", data=data, error=error, url=url)

@app.route("/download")
def download():
    if os.path.exists(DATA_CSV):
        return send_file(DATA_CSV, as_attachment=True)
    return "No file to download", 404

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL3_TASK1_PORT", 1010)))
