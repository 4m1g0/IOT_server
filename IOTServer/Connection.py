from multiprocessing import Process
from abc import abstractmethod
import socket

BUFFER_SIZE = 4096
ID_PREFIX = b'ID: '

class Connection(Process):
    
    def __init__(self, ip, port, socket, din, dout, lock):
        Process.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.din = din
        self.dout = dout
        self.id = ''
        self.lock = lock
        self.idString = b''
        print("[+][" + self.__class__.__name__ + "] New thread started for " + ip + ":" + str(port))
        
    def run(self):
        self.socket.settimeout(0.01)
        while(1):
            try:
                msg = self.socket.recv(4096)
                if not msg: break
                self.lock.acquire()
                try:
                    self.handleIn(msg)
                finally:
                    self.lock.release()
                print("[" + self.__class__.__name__ + "]received: ", str(msg))
                continue
            except socket.timeout:
                pass
            except socket.error as e:
                if e.errno == socket.errno.ECONNRESET:
                    print("[" + self.__class__.__name__ + "] Connection reset.")
                    break
                raise
            
            try:
                self.lock.acquire()
                try:
                    data = self.handleOut()
                finally:
                    self.lock.release()
                self.socket.send(data)
            except QueueEmpty:
                pass
        
        print("[-][" + self.__class__.__name__ + "] Thread closed " + self.ip + ":" + str(self.port))
        self.socket.close()
    
    def trimQueue(self, queue):
        if len(queue) > BUFFER_SIZE:
            queue = queue[(BUFFER_SIZE / 2):]
        return queue
            
    def cleanQueue(self, queue):
        return b''
    
    def addMsgQueue(self, queue, msg):
        return queue + msg
    
    def popQueue(self, queue):
        return queue, self.cleanQueue(queue)
    
    def findId(self, msg):
        index = msg.find(ID_PREFIX)
        if index >= 0:
            identifier = msg[index+4:msg.find(b"\n", index+4)]
            return identifier.rstrip(b'\r\n')
    
    def cleanAndInitializeQueues(self, id):
        if id in self.din:
            del self.din[id]
        
        self.din[id] = b''
        
        if id in self.dout:
            del self.dout[id]
        
        self.dout[id] = b''
    
    @abstractmethod
    def handleIn(self, msg): pass
    
    @abstractmethod
    def handleOut(self): pass
    
# Exception raised when trying to read empty queue
class QueueEmpty(Exception):
    pass
