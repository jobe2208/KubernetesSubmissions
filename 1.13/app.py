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

TODOS = [
    "Learn Kubernetes basics",
    "Deploy application to cluster",
    "Configure persistent volumes",
]


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

            temp_path = IMAGE_PATH + ".tmp"

            with open(temp_path, "wb") as f:
                f.write(response.content)

            os.replace(temp_path, IMAGE_PATH)

            with open(TIMESTAMP_PATH, "w") as f:
                f.write(str(time.time()))

            print("Image cache updated successfully.", flush=True)

        except Exception as e:
            print(f"Image update failed: {e}", flush=True)

            if not image_exists:
                raise

    return IMAGE_PATH


@app.route("/")
def home():
    try:
        get_cached_image()
    except Exception:
        return "No cached image available yet.", 503

    todo_html = "".join(
        f"<li>{todo}</li>" for todo in TODOS
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 40px auto;
                padding: 20px;
                background: #f5f5f5;
            }}

            h1, h2 {{
                text-align: center;
            }}

            img {{
                display: block;
                width: 260px;
                height: 260px;
                object-fit: cover;
                margin: 30px auto;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }}

            .todo-form {{
                display: flex;
                justify-content: center;
                gap: 10px;
                margin: 50px 0 30px;
            }}

            input {{
                width: 550px;
                padding: 14px;
                font-size: 18px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
            }}

            button {{
                padding: 12px 25px;
                font-size: 18px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}

            ul {{
                list-style: none;
                padding: 0;
            }}

            li {{
                background: #fff;
                padding: 22px;
                margin: 10px 0;
                border-left: 5px solid #4CAF50;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>

    <body>
        <h1>Todo App</h1>

        <img src="/image" alt="Random image">

        <div class="todo-form">
            <input
                type="text"
                maxlength="140"
                placeholder="Enter a new todo (max 140 characters)"
            >
            <button type="button">Send</button>
        </div>

        <h2>Todos</h2>
        <ul>
            {todo_html}
        </ul>
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