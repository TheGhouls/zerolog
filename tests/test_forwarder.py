import time
import socket
from multiprocessing import Process
from unittest.mock import patch

import zmq
import pytest

from zerolog.forwarder import start_forwarder


@pytest.fixture
def forwarder():
    """Return a process for forwarder"""
    p = Process(target=start_forwarder, args=(6002, 6001, 6500))
    return p


@pytest.fixture
def context(request):
    context = zmq.Context()

    def fin():
        context.destroy()

    request.addfinalizer(fin)
    return context


@pytest.fixture
def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


@pytest.mark.timeout(5)
def test_forwarder(forwarder, context, sender):
    """Monitor socket should correctly send data"""
    forwarder.start()

    # waiting for warmup
    time.sleep(1)

    mon = context.socket(zmq.SUB)
    mon.setsockopt_string(zmq.SUBSCRIBE, "")
    mon.connect("tcp://localhost:6500")

    recv = context.socket(zmq.SUB)
    recv.setsockopt_string(zmq.SUBSCRIBE, "")
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

    forwarder.terminate()


@patch('zerolog.forwarder.run_proxy')
@pytest.mark.timeout(2)
def test_forwarder_basic_run(run_proxy):
    """Test default forwarder call"""
    start_forwarder(0, 0)


@patch('zerolog.forwarder.run_proxy')
@pytest.mark.timeout(2)
def test_forwarder_run_without_monitor(run_proxy):
    """Test default forwarder call without monitor"""
    start_forwarder(0, 0)
