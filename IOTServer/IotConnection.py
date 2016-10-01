#
# IotConnection.py - Class to handle connections from iot devices
# Copyright 2016 Oscar Blanco.
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version
# 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#

from Connection import Connection, QueueEmpty

BUFFER_SIZE = 4096

class IotConnection(Connection):

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
                self.cleanAndInitializeQueues(self.id)
                print("[" + self.__class__.__name__ + "]Instantiated queues for id: " + str(self.id) + " connection: " + self.ip + ":" + str(self.port))
                end = self.idString.index(identifier)+len(identifier)+1
                if len(self.idString) > end:
                    msg = self.idString[end:].lstrip(b'\r\n')
                else:
                    return
            else:
                index = self.idString.rfind(b'\n')
                if index >= 0:
                    self.idString = self.idString[index:]
                    
                return
        
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
