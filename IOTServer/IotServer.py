from Server import Server
from IotConnection import IotConnection
import time

class IotServer(Server):
    
    def createConnection(self, ip, port, sock):
        service = IotConnection(ip, port, sock, self.din, self.dout, self.lock)
        service.start()
