import time

import zmq
import pytest


@pytest.fixture
def context():
    return zmq.Context()


@pytest.fixture
def sender_socket(context):
    s = context.socket(zmq.PUB)
    s.bind("tcp://*:7000")
    return s


@pytest.fixture
def worker_socket(context):
    s = context.socket(zmq.PULL)
    s.connect("tcp://localhost:7005")


@pytest.fixture
def receiver():
    return None


def test_receiver_recv(context, sender_socket, receiver):
    """Receiver should be able to correctly receive messages"""
    sender_socket.send_string("test data")
    data = receiver.recv_data()
    assert data is not None


def test_receiver_sendback(context, sender_socket, worker_socket):
    """Receiver should be able to sendback messages to workers"""
    sender_socket.send_string("test data")
    data = receiver.recv_data()
    receiver.process(data)

    data = worker_socket.recv()

    assert data is not None
