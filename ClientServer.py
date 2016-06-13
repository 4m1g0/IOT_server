from Server import Server

class ClientServer(Server):
    
    def createConnection(self, ip, port, sock):
        service = ClientConnection(ip, port, sock, self.din, self.dout)
        service.start()
