from Connection import Connection, QueueEmpty

class ClientConnection(Connection):

    def handleIn(self, msg):
        identifier = self.findId(msg)
        if identifier:
            self.id = identifier
        else:
            if self.id in self.din:
                self.din[self.id] = self.addMsgQueue(self.din[self.id], msg)
            else:
                print("[" + self.__class__.__name__ + "] out Queue not instantiated for connection " + self.ip + ":" + str(self.port))
    
    def handleOut(self):
        if self.id in self.dout and self.dout[self.id]:
            data, self.dout[self.id] = self.popQueue(self.dout[self.id])
            return data
        else:
            #print("in Queue not instantiated for connection " + self.ip + " port: " + str(self.port))
            raise QueueEmpty
