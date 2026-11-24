from http.server import BaseHTTPRequestHandler, HTTPServer

counter = 0

class PingPongHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter

        if self.path == "/pingpong":
            response = f"pong {counter}"
            counter += 1

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("0.0.0.0", 8080), PingPongHandler)
print("Ping-pong application running on port 8080", flush=True)
server.serve_forever()
