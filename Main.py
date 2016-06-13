#!/usr/bin/env python

from multiprocessing import Manager
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

with Manager() as manager:
    din = manager.dict()
    dout = manager.dict()

    iotServer = IotServer(tcp_ip, iot_port, din, dout)
    iotServer.start()

    clientServer = ClientServer(tcp_ip, client_port, din, dout)
    clientServer.start()

    iotServer.join()
    clientServer.join()
