from http.server import BaseHTTPRequestHandler, HTTPServer

FILE_PATH = "/usr/src/app/files/log.txt"

class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(FILE_PATH, "r") as file:
                    content = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(content.encode())

            except FileNotFoundError:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Log file has not been created yet")

        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("0.0.0.0", 8080), LogHandler)
print("Log reader running on port 8080", flush=True)
server.serve_forever()