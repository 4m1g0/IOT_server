from multiprocessing import Process
import queue
import socket

BUFFER_SIZE = 4096

class IotConnection(Process):
    
    def __init__(self, ip, port, socket, din, dout):
        Process.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.din = din
        self.dout = dout
        self.id = ''
        print("[+] New thread started for " + ip + ":" + str(port))
        
    def run(self):
        self.socket.settimeout(0.01)
        while(1):
            try:
                msg = self.socket.recv(4096)
                if not msg: break
                self.handleIn(msg)
                print("received: ", str(msg))
                continue
            except socket.timeout:
                pass
            
            try:
                data = self.handleOut()
                self.socket.send(data)
            except queue.Empty:
                pass
        
        print("[-] Thread closed " + self.ip + ":" + str(self.port))
        self.socket.close()
    
    def cleanAndInitialize(self, d, id):
        if id in d:
            del d[id]
        
        d[id] = ''
    
    def handleIn(self, msg):
        if msg.startswith(bytes("ID: ", 'UTF-8')):
            self.id = msg[4:]
            if not self.id: return
            self.cleanAndInitialize(self.dout, self.id)
            self.cleanAndInitialize(self.din, self.id)
            print("Instantiated queues for id: " + str(self.id) + " connection: " + self.ip + ":" + str(self.port))
        else:
            if self.id in self.dout:
                self.dout[self.id] = msg
            else:
                print("out Queue not instantiated for connection " + self.ip + ":" + str(self.port))
    
    def handleOut(self):
        if self.id in self.din and self.din[self.id]:
            return self.din[self.id]
        else:
            #print("in Queue not instantiated for connection " + self.ip + " port: " + str(self.port))
            raise queue.Empty
                
                
                
