import os
from flask import Flask

app = Flask(__name__)

PORT = int(os.getenv("PORT", 8080))

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Todo Application</title>
        </head>
        <body>
            <h1>Todo Application</h1>
            <p>My application is running inside Kubernetes!</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)