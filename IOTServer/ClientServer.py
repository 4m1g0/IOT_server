from Server import Server
from ClientConnection import ClientConnection

class ClientServer(Server):
    
    def createConnection(self, ip, port, sock):
        service = ClientConnection(ip, port, sock, self.din, self.dout, self.lock)
        service.start()
