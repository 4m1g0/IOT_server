from http.server import BaseHTTPRequestHandler, HTTPServer
from RESTMethods.prices import *
import sys
import time

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        Prices(self).do_GET();
    def do_POST(self):
        Prices(self).do_GET();

if __name__ == "__main__":
    hostPort = 80
    if (len(sys.argv) > 1):
        hostPort = int(sys.argv[1])
        
    apiServer = HTTPServer(('', hostPort), APIHandler)
    print(time.asctime(), "Server Starts - %s" % hostPort)

    try:
        apiServer.serve_forever()
    except KeyboardInterrupt:
        pass

    apiServer.server_close()
    print(time.asctime(), "Server Stops - %s" %  hostPort)
