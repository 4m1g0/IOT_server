#
# Server.py - Abstract class to listen for connections
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

from multiprocessing import Process
from abc import abstractmethod
import socket

class Server(Process):
    
    def __init__(self, ip, port, din, dout, lock):
        super().__init__()
        self.ip = ip
        self.port = port
        self.din = din
        self.dout = dout
        self.lock = lock
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)
        
        while(1):
            (sock, (ip, port)) = s.accept()
            self.createConnection(ip, port, sock)
            
    @abstractmethod
    def createConnection(self, ip, port, sock): pass

