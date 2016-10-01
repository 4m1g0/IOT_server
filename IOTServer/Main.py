#!/usr/bin/env python
#
# Main.py - Entry point for the application
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

from multiprocessing import Manager, Lock
from IotServer import IotServer
from ClientServer import ClientServer

import sys
import time

tcp_ip = '0.0.0.0'

if len(sys.argv) < 3:
    print("usage: socket IotPort ClientPort")
    exit(0)

iot_port = int(sys.argv[1])
client_port = int(sys.argv[2])
lock = Lock()

with Manager() as manager:
    din = manager.dict()
    dout = manager.dict()

    iotServer = IotServer(tcp_ip, iot_port, din, dout, lock)
    iotServer.start()

    clientServer = ClientServer(tcp_ip, client_port, din, dout, lock)
    clientServer.start()

    iotServer.join()
    clientServer.join()
