#!/usr/bin/env python
# Inspired by  https://stackoverflow.com/a/25708957/51280
# https://gist.github.com/opyate/6e5fcabc6f41474d248613c027373856
from http.server import SimpleHTTPRequestHandler
import socketserver

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")


if __name__ == '__main__':
    with socketserver.TCPServer(("", 4000), MyHTTPRequestHandler) as httpd:
        print("serving at port", 4000)
        httpd.serve_forever()
