from http.server import BaseHTTPRequestHandler, HTTPServer

FILE_PATH = "/usr/src/app/files/pingpong.txt"


def read_counter():
    try:
        with open(FILE_PATH, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


def write_counter(counter):
    with open(FILE_PATH, "w") as file:
        file.write(str(counter))


class PingPongHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        # Existing ping-pong functionality
        if self.path == "/pingpong":
            counter = read_counter()

            response = f"pong {counter}"
            write_counter(counter + 1)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())

        # New endpoint for other pods to read the counter
        elif self.path == "/pings":
            counter = read_counter()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(str(counter).encode())

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer(("0.0.0.0", 8080), PingPongHandler)
print("Ping-pong application running on port 8080", flush=True)
server.serve_forever()