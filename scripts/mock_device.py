#!/bin/env python

from argparse import ArgumentParser
import sys

import os, pty
import threading

import time
import select

import device_handlers

class MockDevice(threading.Thread) :
    def __init__(self, device_type, *args, **kwargs) :
        super(MockDevice, self).__init__(*args, **kwargs)
        self.port : str = ""
        self.master = None
        self.slave = None
        self._stop_event = threading.Event()
        self._device = device_handlers.Device(device_type)

    def stop(self) :
        self._stop_event.set()

    def stopped(self) :
        return self._stop_event.isSet()

    def open(self) :
        print("Opening MockDevice...")
        self.master, self.slave = pty.openpty()
        self.port = os.ttyname(self.slave)
        print(f"Listen port: {self.port} (fd={self.slave})")
        return self.port
    
    def close(self) :
        os.close(self.slave)

    def run(self) :
        inputs, outputs, messages = [self.master], [], {}
        try :
            while inputs :
                if self.stopped() :
                    break
                readable, _, _ = select.select(inputs, outputs, inputs)
                for _ in readable :
                    cmd = os.read(self.master, 1000)
                    cmd = cmd.decode("utf-8").strip()
                    print(f">> device received: {cmd}")
                    reply_handle = self._device.handle_cmd(cmd)
                    print(f">> reply_handle --> {reply_handle}")
                    reply_handle = reply_handle()
                    print(f"reply_handle evaluated = {reply_handle}")
                    if reply_handle is None :
                        reply = ""
                    else :
                        reply = str(reply_handle)
                    # add termination, should be made a configuration
                    reply += "\r\n"
                    print(f" sending as string: {reply}")
                    encoded = str.encode(str(reply))#, "utf-8")
                    print(f"-> encoded = {encoded}")
                    os.write(self.master, encoded)
        finally :
            print("MockDevice shutting down...")
