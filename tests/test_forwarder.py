import time
import socket
from multiprocessing import Process
from unittest.mock import patch

import zmq
import pytest

from zerolog.forwarder import start_forwarder


@pytest.fixture(scope='module')
def forwarder():
    """Return a process for forwarder"""
    p = Process(target=start_forwarder, args=(6002, 6001, 6500))
    p.start()
    time.sleep(1)
    return p


@pytest.fixture(scope='module')
def tcp_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def test_forwarder(forwarder, tcp_sender, context):
    """Monitor should correctly send data"""
    sender = tcp_sender

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
    sender.close()
    forwarder.terminate()


@patch('zerolog.forwarder.zmq.proxy')
@patch('zerolog.forwarder.zmq.Context')
@patch('zerolog.forwarder.zmq.Context.socket')
@patch('zerolog.forwarder.zmq.Socket')
@patch('zerolog.forwarder.zmq.Socket.bind')
def test_forwarder_basic_run(*args):
    """forwarder should correctly run with different parameters"""
    start_forwarder(6010, 6011, 6012)
    start_forwarder(6020, 6021)
