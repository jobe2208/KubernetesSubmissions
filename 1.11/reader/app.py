from http.server import BaseHTTPRequestHandler, HTTPServer

FILE_PATH = "/usr/src/app/files/log.txt"
PINGPONG_FILE = "/usr/src/app/files/pingpong.txt"


def read_pingpong_counter():
    try:
        with open(PINGPONG_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "0"


class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(FILE_PATH, "r") as file:
                    content = file.read()

            except FileNotFoundError:
                content = "Log file has not been created yet\n"

            counter = read_pingpong_counter()
            response = f"{content}\nPing / Pongs: {counter}"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer(("0.0.0.0", 8080), LogHandler)
print("Log reader running on port 8080", flush=True)
server.serve_forever()