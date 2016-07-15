import time

import zmq
import pytest

from zerolog.receiver import Receiver


@pytest.fixture
def context():
    return zmq.Context()


@pytest.fixture
def sender_socket(context):
    s = context.socket(zmq.PUB)
    s.bind("tcp://*:6700")
    return s


@pytest.fixture
def worker_socket(context):
    s = context.socket(zmq.PULL)
    s.connect("tcp://127.0.0.1:6705")
    return s


@pytest.fixture
def receiver():
    return Receiver("127.0.0.1", 6700, output_port=6705)


@pytest.mark.timeout(10)
def test_receiver(context, sender_socket, receiver, worker_socket):
    """Receiver should be able to correctly receive messages and send them back"""
    sender_socket.send_multipart([b"test", b"data"])
    data = receiver.recv_data()
    assert data is not None

    time.sleep(1)
    receiver.ventilator.send(data)

    data = worker_socket.recv()
    assert data is not None
