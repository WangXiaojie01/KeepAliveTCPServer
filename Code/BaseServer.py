
#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.04.11
author: wangxiaojie
'''

import os, socket, threading, sys
import time
from ThreadClient import ThreadClient

class BaseServer(object):
    def __init__(self):
        self.socket = None
        self.clients = [] 
        self.ip = None 
        self.port = None 
        self.listenNum = 30
        self.sleepTime = 1
        self.clientAddresses = set()
        for i in range(0, self.listenNum):
            self.clients.append(ThreadClient())

    def init(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(self.listenNum)

    def networkUpdate(self):
        print("networkUpdate networkUpdate begin")
        while True:
            self.onUpdate()
            time.sleep(self.sleepTime)

    def accpetConnection(self):
        print("accpetConnection accpetConnection begin")
        def resetClient(addr):
            if addr in self.clientAddresses:
                self.clientAddresses.remove(addr)
        while True:
            connection, address = self.socket.accept()
            if not address in self.clientAddresses:
                for client in self.clients:
                    if not client.hasInit:
                        client.init(connection, address)
                        client.setResetCallback(resetClient)
                        self.clientAddresses.add(address)
                        break
                if not address in self.clientAddresses:
                    connection.send(b"_Client_Overload_")

    def onUpdate(self):
        for client in self.clients:
            client.sendBuffer("onUpdate from sever")# to %s:%s\n" % (client.address[0], client.address[1]))
            
    def run(self):
        try:
            acceptThreading = threading.Thread(target=self.accpetConnection, args=())
            acceptThreading.start()
            updateThreading = threading.Thread(target=self.networkUpdate, args=())
            updateThreading.start()
        except Exception as e:
            print("run start thread error %s" % (str(e))) 
            
if __name__ == "__main__":
    server = BaseServer()
    server.init('localhost', 8001)
    server.run()
