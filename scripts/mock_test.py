#!/bin/env python

from argparse import ArgumentParser
import sys

import os, pty
import io
from serial import Serial
import threading

from dataclasses import dataclass
from typing import Dict, List, Callable, Any, cast, get_type_hints, Optional
import time
import select

class MockDevice(threading.Thread) :
    def __init__(self, *args, **kwargs):
        super(MockDevice, self).__init__(*args, **kwargs)
        self.listen_port : str = ""
        self.master = None
        self.slave = None

        self._stop_event = threading.Event()

    def stop(self) :
        self._stop_event.set()
    def stopped(self) :
        return self._stop_event.is_set()

    def open(self) :
        print("Opening pty")
        master, slave = pty.openpty()
        self.master = master
        self.slave = slave
        self.listen_port = os.ttyname(slave)
        print(f"Slave (listen) port is: {self.listen_port}")
        return self.listen_port
    def close(self) :
        print(f"closing master")
        os.close(self.slave)

    #def start(self) :
    #    thread = threading.Thread(target = self.listen)
    #    thread.start()
    def run(self, stop_thread) :
        print("Starting to listen") #self._stop_listening.clear()
        inputs = [self.master]
        outputs = []
        message_queues = {}
        try :
            while inputs :
                #print(f">> waiting for the next event")
                readable, writeable, exceptional = select.select(inputs, outputs, inputs)
                for s in readable :
                    cmd = os.read(self.master, 8 * 3)
                    print(f">> readable = {s}, cmd = {cmd}")
                    os.write(self.master, b"FOOBLY 1\r\n")
                    os.fsync(self.master)
                    os.write(self.master, b"FOOBLY 2\r\n")
                    os.fsync(self.master)

        #try :
        #    while True :
        #        #if self.stopped() :
        #        if stop_thread() :
        #            break
        #        cmd = b""
        #        while not cmd.endswith(b"\r\n") :
        #            if stop_thread() :
        #                break
        #            cmd += os.read(self.master, 1)
        #        cmd = cmd.decode("utf-8").strip()
        #        print(f"Device received: {cmd}")
        #        if cmd == "MOCK:KILL" :
        #            print("Mock device has received KILL command, stopping")
        #            break
        finally :
            print(f"Device has stopped listening at port \"{self.listen_port}\"")
    
    

def main() :
    hw = MockDevice()
    port = hw.open()
    print(f"hw port = {port}")

    #hw.start()
    stop_thread = False
    t = threading.Thread(target = hw.run, args = (lambda : stop_thread,))
    t.start()
    #hw.start()

    #ser = Serial(port, 115200, timeout=0.1)
    #print(f"Opening serial port for communication with device at {port}")
    #cmds = [b"Hello, world\r\n", b"Hello, world\r\n", b"Hello, world\r\n"]#, b"MOCK:KILL\r\n"]
    #for cmd in cmds :
    #    ser.write(cmd)

    #    time.sleep(0.5)
    #    response = ser.read(100)
    #    print(f"response = {response}")

    input("Press any button to stop device")
    sys.exit()
    print(f"done sending, will wait 1 second")
    time.sleep(1)
    print(f"setting stop_thread flag")
    stop_thread = True
    time.sleep(1)

    #cmd = b"MOCK:KILL"
    #ser.write(cmd)

    #hw.kill()
    #hw.stop()
    t.join()
    #hw.close()
    #hw.join()
    #hw.kill()= Serial(s_name, 2400, timeout=1)
# 33#    ser.write(b'test2\r\n') #write the first command
# 34     res = b""
# 35     while not res.endswith(b'\r\n'):
# 36         #read the response
# 37         res +=ser.read()
# 38     print("result: %s" % res)
# 39     ser.write(b'QPGS\r\n') #write a second command
# 40     res = b""
# 41     while not res.endswith(b'\r\n'):
# 42         #read the response
# 43         res +=ser.read()


if __name__ == "__main__" :
    main()


#  1 import os, pty
#  2 from serial import Serial
#  3 import threading
#  4
#  5 def listener(port):
#  6     #continuously listen to commands on the master device
#  7     while 1:
#  8         res = b""
#  9         while not res.endswith(b"\r\n"):
# 10             #keep reading one byte at a time until we have a full line
# 11             res += os.read(port, 1)
# 12         print("command: %s" % res)
# 13
# 14         #write back the response
# 15         if res == b'QPGS\r\n':
# 16             os.write(port, b"correct result\r\n")
# 17         else:
# 18             os.write(port, b"I dont understand\r\n")
# 19
# 20 def test_serial():
# 21     """Start the testing"""
# 22     master,slave = pty.openpty() #open the pseudoterminal
# 23     s_name = os.ttyname(slave) #translate the slave fd to a filename
# 24     #print(f"master name: {os.ttyname(master)}")
# 25     print(f"slave name : {os.ttyname(slave)}")
# 26
# 27     #create a separate thread that listens on the master device for commands
# 28     thread = threading.Thread(target=listener, args=[master])
# 29     thread.start()
# 30
# 31     #open a pySerial connection to the slave
# 32     ser = Serial(s_name, 2400, timeout=1)
# 33     ser.write(b'test2\r\n') #write the first command
# 34     res = b""
# 35     while not res.endswith(b'\r\n'):
# 36         #read the response
# 37         res +=ser.read()
# 38     print("result: %s" % res)
# 39     ser.write(b'QPGS\r\n') #write a second command
# 40     res = b""
# 41     while not res.endswith(b'\r\n'):
# 42         #read the response
# 43         res +=ser.read()
# 44     print("result: %s" % res)
# 45
# 46 if __name__=='__main__':
# 47     test_serial()
#~
#~