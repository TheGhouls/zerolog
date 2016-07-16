import os
import time
from unittest.mock import patch

import zmq
import pytest

from zerolog.receiver import Receiver

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def test_main_receiver(context):
    """Receiver should correctly run"""
    sender = context.socket(zmq.PUB)
    sender.bind("tcp://127.0.0.1:6700")

    worker = context.socket(zmq.PULL)
    worker.connect("tcp://127.0.0.1:6200")

    time.sleep(1)

    receiver = Receiver("127.0.0.1", 6700, output_port=6200)

    sender.send_multipart([b"topic", b"test"])
    data = receiver.recv_data()

    assert data is not None

    receiver.ventilator.send(data)
    data = worker.recv()

    assert data is not None

    sender.send_multipart([b"topic", b"test"])
    receiver.ventilator = None  # remove socket to force exception to be raised

    with pytest.raises(AttributeError):
        receiver.run()


@patch('zerolog.receiver.zmq.Context.socket')
def test_receiver_error(socket):
    """Receiver should correctly raise errors"""
    with pytest.raises(TypeError):
        Receiver("127.0.0.1", 6700, output_port=0, output_socket="bad.sock")


@patch('zerolog.receiver.zmq.Context.socket')
def test_receiver_ipc(socket):
    """Receiver should be able to use ipc socket"""
    Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")


@patch('zerolog.receiver.zmq.Context.socket')
def test_receiver_no_args(socket):
    """Receiver should be able to instanciate without output arguments"""
    Receiver("127.0.0.1", 6700)


@patch('zerolog.receiver.zmq.Socket.bind')
def test_receiver_log_config(bind):
    """Receiver should be able to use logging configuration file"""
    cf = os.path.join(BASE_DIR, "fixtures/log.cfg")
    Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock", logging_config=cf)
