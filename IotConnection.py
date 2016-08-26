from Connection import Connection, QueueEmpty

BUFFER_SIZE = 4096

class IotConnection(Connection):

    def handleIn(self, msg):
        identifier = self.findId(msg)
        if identifier:
            self.id = identifier
            self.cleanAndInitializeQueues(self.id)
            end = msg.index(identifier)+len(identifier)+1
            if len(msg) > end:
                msg = msg[end:]
            print("[" + self.__class__.__name__ + "]Instantiated queues for id: " + str(self.id) + " connection: " + self.ip + ":" + str(self.port))
        
        if self.id in self.dout:
            self.dout[self.id] = self.addMsgQueue(self.dout[self.id], msg)
        else:
            print("[" + self.__class__.__name__ + "]out Queue not instantiated for connection " + self.ip + ":" + str(self.port))
    
    def handleOut(self):
        if self.id in self.din and self.din[self.id]:
            data, self.din[self.id] = self.popQueue(self.din[self.id])
            return data
        else:
            #print("in Queue not instantiated for connection " + self.ip + " port: " + str(self.port))
            raise QueueEmpty
