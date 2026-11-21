import os
from flask import Flask

app = Flask(__name__)

PORT = int(os.getenv("PORT", 8080))

@app.route("/")
def home():
    return "Server started"

if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)