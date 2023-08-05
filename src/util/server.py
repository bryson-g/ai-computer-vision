import http.server as serv
from util.capture import save_frame
import json

# curl -X POST http://localhost:8080/api/picture -H "Content-Type: application/json" -d "{\"savePath\":\"C:/Users/bglembin/Desktop/test.jpg\"}"


class RequestHandler(serv.BaseHTTPRequestHandler):
    def run(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        print(data)
        save_frame(data['savePath'])

    def do_POST(self):
        if self.path == "/api/picture":
            try:
                self.run()
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print(e)
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("404 Not found".encode("utf-8"))

def open_server():
    server = serv.HTTPServer(("localhost", 8080), RequestHandler)
    print("Server opened.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    
    print("Server closed.")

if __name__ == "__main__":
    open_server()