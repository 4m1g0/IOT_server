from Connection import Connection
import queue

BUFFER_SIZE = 4096

class IotConnection(Connection):
    
    def cleanAndInitialize(self, d, id):
        if id in d:
            del d[id]
        
        d[id] = b''
    
    def handleIn(self, msg):
        if msg.startswith(bytes("ID: ", 'UTF-8')):
            self.id = msg[4:]
            if not self.id: return
            self.cleanAndInitialize(self.dout, self.id)
            self.cleanAndInitialize(self.din, self.id)
            print("[" + self.__class__.__name__ + "]Instantiated queues for id: " + str(self.id) + " connection: " + self.ip + ":" + str(self.port))
        else:
            if self.id in self.dout:
                self.dout[self.id] += msg
            else:
                print("[" + self.__class__.__name__ + "]out Queue not instantiated for connection " + self.ip + ":" + str(self.port))
    
    def handleOut(self):
        if self.id in self.din and self.din[self.id]:
            data = self.din[self.id]
            self.din[self.id] = b''
            return data
        else:
            #print("in Queue not instantiated for connection " + self.ip + " port: " + str(self.port))
            raise queue.Empty
