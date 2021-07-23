import json
import os
import socket
import subprocess
import threading

from nuxhash.devices.nvidia import NvidiaDevice
from nuxhash.miners import miner
from nuxhash.utils import get_port


ALGORITHMS = [
    'equihash',
    'pascal',
    'decred',
    'blake2s',
    'daggerhashimoto',
    'lyra2rev2',
    'daggerhashimoto_decred',
    #'daggerhashimoto_sia',
    'daggerhashimoto_pascal'
    ]
NHMP_PORT = 3200


class ExcavatorError(Exception):
    pass


class ExcavatorAPIError(ExcavatorError):
    """Exception returned by excavator."""

    def __init__(self, response):
        self.response = response
        self.error = response['error']


class ExcavatorServer(object):

    BUFFER_SIZE = 1024
    TIMEOUT = 10

    def __init__(self, executable):
        self._executable = executable
        self.__subscription = self._process = None
