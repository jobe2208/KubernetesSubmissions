from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen

FILE_PATH = "/usr/src/app/files/log.txt"
PING_PONG_URL = "http://ping-pong-2-1-svc:8080/pings"


def get_pings():
    try:
        with urlopen(PING_PONG_URL, timeout=3) as response:
            return response.read().decode()
    except Exception as e:
        return f"Unable to reach Ping Pong: {e}"


class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(FILE_PATH, "r") as file:
                    content = file.read()
            except FileNotFoundError:
                content = "Log file has not been created yet"

            pings = get_pings()

            output = f"{content}\nPing / Pongs: {pings}"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(output.encode())

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer(("0.0.0.0", 8080), LogHandler)
print("Log reader running on port 8080", flush=True)
server.serve_forever()