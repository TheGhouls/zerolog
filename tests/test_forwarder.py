import time
import socket
from multiprocessing import Process

import zmq
import pytest

from zerolog.forwarder import start_forwarder


@pytest.fixture
def forwarder():
    """Return a process for forwarder"""
    import multiprocessing
    p = Process(target=start_forwarder, args=(6002, 6001, 6500))
    return p


@pytest.fixture
def context():
    return zmq.Context()


@pytest.fixture
def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


@pytest.mark.timeout(5)
def test_forwarder(forwarder, context, sender):
    """Monitor socket should correctly send data"""
    forwarder.start()
    time.sleep(1)

    mon = context.socket(zmq.SUB)
    mon.setsockopt_string(zmq.SUBSCRIBE, "")
    mon.connect("tcp://localhost:6500")

    recv = context.socket(zmq.SUB)
    recv.setsockopt_string(zmq.SUBSCRIBE, "")
    recv.connect("tcp://localhost:6002")

    server_address = ('localhost', 6001)
    sender.connect(server_address)
    sender.sendall(b"test test")

    data = mon.recv()
    assert data is not None

    sender.sendall(b"test test")

    data = recv.recv()
    assert data is not None

    forwarder.terminate()
