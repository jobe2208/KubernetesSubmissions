
import os
import time
import requests
from flask import Flask, send_file

app = Flask(__name__)

PORT = int(os.getenv("PORT", 8080))

CACHE_DIR = os.getenv("CACHE_DIR", "/usr/src/app/files")
IMAGE_PATH = os.path.join(CACHE_DIR, "cached_image.jpg")
TIMESTAMP_PATH = os.path.join(CACHE_DIR, "cache_timestamp.txt")

CACHE_DURATION = 600  # 10 minutes
IMAGE_URL = "https://picsum.photos/1200"


def get_cached_image():
    os.makedirs(CACHE_DIR, exist_ok=True)

    image_exists = os.path.exists(IMAGE_PATH)
    cache_expired = True

    if image_exists and os.path.exists(TIMESTAMP_PATH):
        with open(TIMESTAMP_PATH, "r") as f:
            last_fetch = float(f.read())

        cache_expired = time.time() - last_fetch > CACHE_DURATION

    if not image_exists or cache_expired:
        print("Fetching a new image from Picsum...", flush=True)

        try:
            response = requests.get(IMAGE_URL, timeout=20)
            response.raise_for_status()

            # Write to a temporary file first so the old image
            # is not lost if downloading or writing fails.
            temp_path = IMAGE_PATH + ".tmp"

            with open(temp_path, "wb") as f:
                f.write(response.content)

            os.replace(temp_path, IMAGE_PATH)

            with open(TIMESTAMP_PATH, "w") as f:
                f.write(str(time.time()))

            print("Image cache updated successfully.", flush=True)

        except Exception as e:
            print(f"Image update failed: {e}", flush=True)

            # If we already have an image, keep using it.
            if not image_exists:
                raise

    return IMAGE_PATH


@app.route("/")
def home():
    try:
        get_cached_image()
    except Exception:
        return "No cached image available yet.", 503

    return """
    <html>
        <head>
            <title>Todo Application</title>
        </head>
        <body>
            <h1>Todo Application</h1>
            <p>My application is running inside Kubernetes!</p>
            <h2>Random image</h2>
            <img src="/image" width="600">
        </body>
    </html>
    """


@app.route("/image")
def image():
    try:
        image_path = get_cached_image()
        return send_file(image_path, mimetype="image/jpeg")
    except Exception:
        return "No cached image available.", 503


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)
