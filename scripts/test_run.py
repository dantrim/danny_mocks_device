#!/bin/env python

from mock_device import MockDevice
import device_handlers

def main() :

    device = MockDevice(device_type = "SCPI")
    port = device.open()
    print(f"Opened port: {port}")
    device.start()
    input()

if __name__ == "__main__" :
    main()
