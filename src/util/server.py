import http.server as serv
from urllib.parse import urlparse, parse_qs
from util.capture import save_frame

# curl -X POST http://localhost:8080/api/picture -H "Content-Type: application/json" -d "{\"savePath\":\"C:/Users/bglembin/Desktop/test.jpg\"}"


class RequestHandler(serv.BaseHTTPRequestHandler):
    def run(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query) 
        save_frame(params['saveTo'][0])

    def do_POST(self):
        try:
            self.run()
            self.send_response(200)
            self.end_headers() 
        except Exception as e:
            print(e)
            self.send_response(500)
            self.end_headers()

def open_server():
    server = serv.HTTPServer(("localhost", 8094), RequestHandler)
    print("Server opened.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    
    print("Server closed.")

if __name__ == "__main__":
    open_server()