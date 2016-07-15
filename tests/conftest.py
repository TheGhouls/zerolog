import time
import socket

import zmq
import pytest

from zerolog.receiver import Receiver


@pytest.fixture(scope='session')
def context():
    return zmq.Context.instance()


@pytest.fixture(scope='session')
def receiver():
    receiver = Receiver("127.0.0.1", 6700, output_port=6705)
    return receiver


@pytest.fixture(scope='session')
def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock
