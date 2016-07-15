import os
import time
from unittest.mock import patch

import zmq
import pytest

from zerolog.receiver import Receiver

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='module')
def sender_socket(context):
    s = context.socket(zmq.PUB)
    s.bind("tcp://*:6700")
    time.sleep(1)
    return s


@pytest.fixture(scope='module')
def worker_socket(context):
    s = context.socket(zmq.PULL)
    s.connect("tcp://127.0.0.1:6705")
    time.sleep(1)
    return s


def test_receiver(receiver, sender_socket, worker_socket):
    """Receiver should be able to correctly receive messages and send them back"""
    for i in range(10):
        sender_socket.send_multipart([b"", b"data"])
    data = receiver.recv_data()
    assert data is not None

    while data:
        try:
            data = receiver.forwarder.recv(zmq.NOBLOCK)
        except zmq.Again:
            pass

    receiver.ventilator.send(data)

    data = worker_socket.recv()
    assert data is not None


@patch('zerolog.receiver.zmq.Socket.bind')
def test_receiver_error(bind):
    """Receiver should correctly raise errors"""
    with pytest.raises(TypeError):
        Receiver("127.0.0.1", 6700, output_port=0, output_socket="bad.sock")


@patch('zerolog.receiver.zmq.Socket.bind')
def test_receiver_ipc(bind):
    """Receiver should be able to use ipc socket"""
    Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")


@patch('zerolog.receiver.zmq.Socket.bind')
def test_receiver_no_args(bind):
    """Receiver should be able to instanciate without output arguments"""
    r = Receiver("127.0.0.1", 6700)
    r.forwarder.setsockopt(zmq.LINGER, 0)
    r.ventilator.setsockopt(zmq.LINGER, 0)


@patch('zerolog.receiver.zmq.Socket.bind')
def test_receiver_log_config(bind):
    """Receiver should be able to use logging configuration file"""
    cf = os.path.join(BASE_DIR, "fixtures/log.cfg")
    Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock", logging_config=cf)


def test_receiver_run(sender_socket):
    """Receiver run method should correctly run and except"""
    receiver = Receiver("127.0.0.1", 6700, output_socker="/tmp/test.sock")
    receiver.ventilator = None

    sender_socket.send_multipart([b"test", b"data"])
    with pytest.raises(AttributeError):
        receiver.run()
