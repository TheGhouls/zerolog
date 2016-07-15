import time
import socket
from multiprocessing import Process
from unittest.mock import patch

import zmq
import pytest

from zerolog.forwarder import start_forwarder


@pytest.fixture(scope='module')
def forwarder(request):
    """Return a process for forwarder"""
    p = Process(target=start_forwarder, args=(6002, 6001, 6500))
    p.start()
    time.sleep(1)

    def fin():
        p.terminate()

    request.addfinalizer(fin)
    return p


@pytest.fixture(scope='module')
def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def test_forwarder(forwarder, sender):
    """Monitor socket should correctly send data"""
    context = zmq.Context()
    mon = context.socket(zmq.SUB)
    mon.setsockopt_string(zmq.SUBSCRIBE, "")
    mon.setsockopt(zmq.LINGER, 0)
    mon.connect("tcp://localhost:6500")

    recv = context.socket(zmq.SUB)
    recv.setsockopt_string(zmq.SUBSCRIBE, "")
    recv.setsockopt(zmq.LINGER, 0)
    recv.connect("tcp://localhost:6002")

    server_address = ('localhost', 6001)
    sender.connect(server_address)

    # waiting for warmup
    time.sleep(1)

    sender.sendall(b"test test")

    data = mon.recv()
    assert data is not None

    sender.sendall(b"test test")

    data = recv.recv()
    assert data is not None

@patch('zerolog.forwarder.zmq.proxy')
def test_forwarder_basic_run(run_proxy):
    """Test default forwarder calls"""
    start_forwarder(6010, 6011, 6012)
    start_forwarder(6020, 6021)
