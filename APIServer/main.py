from http.server import BaseHTTPRequestHandler, HTTPServer
import xmltodict
import requests
import time
import json
import socket

hostName = ""
hostPort = 9000
server_ip = "137.74.114.25"
server_port = 8081

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        network = self.headers.get('Network-token')
        if not network:
            self.send_response(401)
            self.send_header("Content-Length", 0)
            self.end_headers()
            return

        '''print(self.command + " " + self.path + " " + self.request_version)
        print(self.headers)
        print(self.rfile.read(int(self.headers.get('content-length'))))'''
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))
        s.send(bytes("ID: " + network + "\n", 'utf-8'))
        s.send(bytes(self.command + " " + self.path + " " + self.request_version, 'utf-8'))
        s.send(bytes(str(self.headers), 'utf-8'))
        length = self.headers.get('Content-length')
        if length:
            s.send(self.rfile.read(int(length)))
        data = s.recv(1024)
        s.close()
        self.wfile.write(data)
    
    do_HEAD = do_GET
    do_POST = do_GET
    do_OPTIONS = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
