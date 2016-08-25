from http.server import BaseHTTPRequestHandler, HTTPServer
import xmltodict
import requests
import time
import json

hostName = ""
hostPort = 9000
cache = {}

def getJson(url):
    r = requests.get(url)
    doc = {}
    lista = []
    try:
        doc = xmltodict.parse(r.text)
    
        for i in doc['PVPCDesgloseHorario']['SeriesTemporales'][7]['Periodo']['Intervalo']:
            lista.append(int(float(i['Ctd']['@v']) * 1000000))
    except:
        pass
    return lista
    



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        lista = []
        if self.path[1:] in cache:
            lista = cache[self.path[1:]]
            print("From cache:")
        else:
            lista = getJson("https://api.esios.ree.es/archives/80/download?date=" + self.path[1:])
            cache[self.path[1:]] = lista
        print(lista)
        
        if lista == []:
            self.send_response(404)
        else:
            body = bytes(json.dumps(lista), 'utf-8')
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
