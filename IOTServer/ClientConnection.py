from Connection import Connection, QueueEmpty

class ClientConnection(Connection):

    def handleIn(self, msg):
        if not self.id:
            self.idString += msg
            if self.idString.find(b'\n') < 0:
                if len(self.idString) > 1024:
                    self.idString = ''
                return # keep buffering untill \n
            identifier = self.findId(self.idString)
            if identifier:
                self.id = identifier
                end = self.idString.index(identifier)+len(identifier)
                if len(self.idString) > end:
                    msg = self.idString[end:].lstrip(b'\r\n')
                else:
                    return
            else:
                index = self.idString.rfind(b'\n')
                if index >= 0:
                    self.idString = self.idString[index:]
                    
                return
                
        
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
