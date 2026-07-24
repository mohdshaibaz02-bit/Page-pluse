from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Function to validate URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    url = data.get("url", "").strip()

    # Check if URL is empty
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Check if URL is valid
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    try:

        # Measure response time
        start_time = time.time()

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        end_time = time.time()

        response_time = round((end_time - start_time) * 1000, 2)

        # Check content type
        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type:
            return jsonify({
                "error": "URL is not an HTML page"
            }), 400

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Page Title
        if soup.title:
            title = soup.title.string.strip()
        else:
            title = "No Title"

        # Meta Description
        meta = soup.find("meta", attrs={"name": "description"})

        if meta and meta.get("content"):
            meta_description = meta["content"].strip()
        else:
            meta_description = "No Description"

        # H1 Count
        h1_count = len(soup.find_all("h1"))

        # Images Missing Alt
        images = soup.find_all("img")

        missing_alt = 0

        for img in images:
            if not img.get("alt"):
                missing_alt += 1

        # Word Count
        text = soup.get_text(separator=" ")

        word_count = len(text.split())

        # JSON Response
        return jsonify({
            "status": response.status_code,
            "responseTime": response_time,
            "title": title,
            "metaDescription": meta_description,
            "h1Count": h1_count,
            "missingAltImages": missing_alt,
            "wordCount": word_count
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timed out"
        }), 408

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Unable to fetch the website"
        }), 500

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return "Page Pulse Backend is Running"


if __name__ == "__main__":
    app.run(debug=True)