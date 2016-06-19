from Connection import Connection
import queue

BUFFER_SIZE = 4096

class ClientConnection(Connection):
    
    def handleIn(self, msg):
        if msg.startswith(bytes("ID: ", 'UTF-8')):
            self.id = msg[4:]
            if not self.id: return
        else:
            if self.id in self.din:
                self.din[self.id] += msg
            else:
                print("[" + self.__class__.__name__ + "] out Queue not instantiated for connection " + self.ip + ":" + str(self.port))
    
    def handleOut(self):
        if self.id in self.dout and self.dout[self.id]:
            data = self.dout[self.id]
            self.dout[self.id] = b''
            return data
        else:
            #print("in Queue not instantiated for connection " + self.ip + " port: " + str(self.port))
            raise queue.Empty
