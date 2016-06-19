from multiprocessing import Process
from abc import abstractmethod
import queue
import socket

BUFFER_SIZE = 4096

class Connection(Process):
    
    def __init__(self, ip, port, socket, din, dout):
        Process.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.din = din
        self.dout = dout
        self.id = ''
        print("[+][" + self.__class__.__name__ + "] New thread started for " + ip + ":" + str(port))
        
    def run(self):
        self.socket.settimeout(0.01)
        while(1):
            try:
                msg = self.socket.recv(4096)
                if not msg: break
                self.handleIn(msg)
                print("[" + self.__class__.__name__ + "]received: ", str(msg))
                continue
            except socket.timeout:
                pass
            
            try:
                data = self.handleOut()
                self.socket.send(data)
            except queue.Empty:
                pass
        
        print("[-][" + self.__class__.__name__ + "] Thread closed " + self.ip + ":" + str(self.port))
        self.socket.close()
    
    @abstractmethod
    def handleIn(self, msg): pass
    
    @abstractmethod
    def handleOut(self): pass    
