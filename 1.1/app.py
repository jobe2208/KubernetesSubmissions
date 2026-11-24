import time
import uuid
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

random_string = str(uuid.uuid4())
timestamp = ""

def update_timestamp():
    global timestamp
    while True:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        print(f"{timestamp}: {random_string}", flush=True)
        time.sleep(5)

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            response = f"{timestamp}: {random_string}"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

threading.Thread(target=update_timestamp, daemon=True).start()

server = HTTPServer(("0.0.0.0", 8080), StatusHandler)
print("HTTP server started on port 8080", flush=True)
server.serve_forever()