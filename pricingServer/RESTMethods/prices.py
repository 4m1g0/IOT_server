from .RESTHandler import RESTHandler
import xmltodict
import requests
import json

class Prices(RESTHandler):
    cache = {}

    def __getJson(self, url):
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
    
    def do_GET(self):
        lista = []
        if self.request.path[1:] in Prices.cache:
            lista = Prices.cache[self.request.path[1:]]
            print("From cache:")
        else:
            lista = self.__getJson("https://api.esios.ree.es/archives/80/download?date=" + self.request.path[1:])
            Prices.cache[self.request.path[1:]] = lista
        print(lista)
        
        if lista == []:
            self.request.send_response(404)
        else:
            self.request.send_response(200)
            self.request.send_header("Content-type", "application/javascript")
            self.request.end_headers()
            self.request.wfile.write(bytes(json.dumps(lista), 'utf-8'))

