from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socket
import json 

class MyHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/message':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            send_to_socket(data)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Message sent successfully</h1></body></html>')
        else:
            self.send_error(404, 'Not Found')

def send_to_socket(data):
    HOST = 'localhost'
    PORT = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode(), (HOST, PORT))

def save_data(data):
    with open('storage/data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def main():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, MyHTTPHandler)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()