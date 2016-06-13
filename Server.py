from multiprocessing import Process
from abc import abstractmethod
import socket

class Server(Process):
    
    def __init__(self, ip, port, din, dout):
        super().__init__()
        self.ip = ip
        self.port = port
        self.din = din
        self.dout = dout
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)
        
        while(1):
            (sock, (ip, port)) = s.accept()
            self.createConnection(ip, port, sock)
            
    @abstractmethod
    def createConnection(self, ip, port, sock): pass

