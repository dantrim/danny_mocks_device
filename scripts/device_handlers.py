#!/bin/env python
from typing import Callable, List, Dict

import functools
import re

__tmp_handler_dict__ = {}
class Handlers :
    @classmethod
    def register(cls, device_type: str, re_string: str) -> Callable :
        def decorator(function) :
            if device_type not in __tmp_handler_dict__ :
                __tmp_handler_dict__[device_type] = {}
            __tmp_handler_dict__[device_type][re_string] = function
        return decorator

class SCPIDevice :
    def __init__(self) :
        pass

    # each of the defined methods should be implementations
    # of a base "Device" class, such that the API matches
    # to what labRemote expects...

    # registering the types in the decorators is probably superfluous, since
    # we can just infer the class type

    # the idea is that the device will listen for commands from the user code
    # and then loop over the registered handlers, performing some matching
    # criteria (e.g. regex) against the handler string and the cmd string,
    # and then execute the handler where a match is found
    @staticmethod
    @Handlers.register("SCPI", "VOLT?")
    def meas_voltage() :
        return 125.4

    @staticmethod
    @Handlers.register("SCPI", "INST:NSEL")
    def set_channel() :
        return None

    @staticmethod
    @Handlers.register("SCPI", "IDN?")
    def ping() :
        return "OK"

class CAENDevice :
    def __init__(self) :
        pass

    @staticmethod
    @Handlers.register("CAEN", "V?")
    def meas_voltage() :
        return 4.0

    @staticmethod
    @Handlers.register("CAEN", "$CMD:MON,PAR:BDNAME")
    def ping() :
        return "OK"


def available_command_types() :
    return list(__tmp_handler_dict__.keys())

class Device :
    def __new__(cls, which_device, *args, **kwargs) :
        print(f"in new: args = {which_device}")
        device_class = super().__new__(cls, *args, **kwargs)
        if which_device not in __tmp_handler_dict__ :
            raise Exception(f"No handlers defined for device type \"{which_device}\"")
        device_class.__handler_dict__ = dict(__tmp_handler_dict__[which_device])
        return device_class
    def __init__(self, device_type : str = "") :
        self.device_type = device_type
        pass

    def handle_cmd(self, cmd) :
        print(f"handling input cmd = {cmd}")
        for cmd_pattern in self.__handler_dict__ :
            # search for the pattern in the input cmd, first escaping the meta characters
            cmd_pattern = cmd_pattern.replace("?", "\?")
            if re.search(cmd_pattern, cmd) :
                print(f"found match between cmd_pattern = {cmd_pattern} and input cmd = {cmd}")
                return self.__handler_dict__[cmd]
        raise RuntimeError(f"Device type \"{self.device_type}\" has no handler defined for input command \"{cmd}\"")

def main() :
    print(f"Command sets for devices: {available_command_types()}")
    print(55 * "-")
    d = Device("SCPI")
    cmd = "VOLT?"
    reply = d.handle_cmd(cmd)
    print(f"SCPI reply to cmd = {cmd} is {reply()}")

    c = Device("CAEN")
    cmd = "V?"
    reply = c.handle_cmd(cmd)
    print(f"CAEN reply to cmd = {cmd} is {reply()}")

if __name__ == "__main__" :
    main()
