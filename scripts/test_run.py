#!/bin/env python

from mock_device import MockDevice
import device_handlers

def main() :

    device = MockDevice(device_type = "SCPI")
    port = device.open()
    print(f"Opened port: {port}")
    device.start()
    # need a proper thread halt here!! python does this weird
    device.stop()
    device.join()

if __name__ == "__main__" :
    main()
