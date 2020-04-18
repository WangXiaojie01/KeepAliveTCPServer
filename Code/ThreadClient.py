
#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.04.11
author: wangxiaojie
'''

import os, socket, threading, sys

class ThreadClient(object):
    def __init__(self):
        self.address = None
        self.socket = None
        self.recvBufferSize = 1024
        self.maxFailedTime = 3
        self.failedConnectTime = 0
        self.hasInit = False
        self.recvThread = None
        self.resetCallBack = None

    def init(self, connect, address):
        self.address = address
        self.socket = connect
        self.hasInit = True
        self.recvThread = threading.Thread(target=self.networkRecv, args=())
        self.recvThread.start()

        
    def reset(self):
        try:
            self.socket.close()
        except Exception as e:
            print("close socket error")
        if self.resetCallBack:
            self.resetCallBack(self.address)
        self.address = None
        self.socket = None
        self.hasInit = False
        self.failedConnectTime = 0
        self.resetCallBack = None
        

    def setResetCallback(self, func):
        self.resetCallBack = func

    def recvBuffer(self):
        if self.hasInit and self.socket:
            try:
                buf = self.socket.recv(self.recvBufferSize)
                if len(buf) > 0:
                    return buf
                else:
                    return None
            except Exception as e:
                print("receive buf failed, %s" %str(e))
                self.connectFailed()
                return None
        else:
            return None

    def sendBuffer(self, buf):
        if self.hasInit and self.socket:
            try:
                self.socket.send(buf.encode('gbk'))
                return True
            except Exception as e:
                print("send buf failed")
                self.connectFailed()
                return False
        else:
            return False

    def connectFailed(self):
        self.failedConnectTime += 1
        if self.failedConnectTime >= self.maxFailedTime:
            self.reset()

    def networkRecv(self):
        while True:
            if not self.hasInit:
                return
            buf = self.recvBuffer()
            if buf:
                self.onRecv(buf)

    def onRecv(self, buf):
        pass