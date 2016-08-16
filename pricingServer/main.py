from http.server import BaseHTTPRequestHandler, HTTPServer
import xmltodict
import requests
import time
import json

hostName = ""
hostPort = 9000

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
        lista = getJson("https://api.esios.ree.es/archives/80/download?date=" + self.path[1:])
        
        if lista == []:
            self.send_response(404)
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(lista), 'utf-8'))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
