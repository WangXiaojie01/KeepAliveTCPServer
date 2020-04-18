#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.04.11
author: wangxiaojie
'''

import os, socket, threading, sys
import time

class BaseClient(object):
    def __init__(self):
        print("__init__ new a base client socket")
        self.socket = None
        self.ip = None
        self.port = None
        self.recvBufferSize = 1024
        self.hasInit = False
        self.maxConnectFailedTimes = 3
        self.connectFailedTime = 0
    
    def init(self, ip, port):
        if self.hasInit:
            return
        print("init init a base client, server ip is %s, port is %d"%(ip, port))
        self.ip = ip
        self.port = port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.socket.connect((ip, port))
            self.hasInit = True
        except Exception as e:
            print("ClientSocket init error")
            self.reset()

    def reset(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print("ClientSocket reset error")
            self.socket = None
        self.ip = None
        self.port = None
        self.hasInit = False
        self.connectFailedTime = 0
        
    def networkRecv(self):
        print("networkRecv newworkRecv begin")
        while True:
            if not self.hasInit:
                return
            try:
                bufBytes = self.socket.recv(self.recvBufferSize)
                buf = bufBytes.decode('gbk')
                if len(buf) > 0:
                    print("networkRecv recv buf from server %s" % buf)
                    self.onRecvBeforeSolved(buf)
            except Exception as e:
                print("networkRecv networkRecv exception %s" % str(e))
                self.connectFailed()

    def onRecvBeforeSolved(self, buf):
        print("onRecvBeforeSolved recv from server, buf is %s" % buf)
        if buf == "_Client_Overload_":
            self.reset()
        else:
            self.onRecv(buf)

    def onRecv(self, buf):
        print("onRecv from server, buf is %s" % buf)

    def connectFailed(self):
        self.connectFailed += 1
        if self.connectFailed >= self.maxConnectFailedTimes:
            self.reset()

    def sendBuffer(self, buf):
        if self.hasInit:
            try:
                self.socket.send(buf.encode('gbk'))
                return True
            except Exception as e:
                print("send buf failed")
                return False
        else:
            return False

    def run(self):
        try:
            recvThreading = threading.Thread(target=self.networkRecv, args=())
            recvThreading.start()
        except Exception as e:
            print("run start thread error %s" % (str(e))) 

 
if __name__ == "__main__":  
    client = BaseClient()
    client.init('localhost', 8001)
    client.run()