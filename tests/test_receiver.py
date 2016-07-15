import os
import time

import zmq
import pytest

from zerolog.receiver import Receiver

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def context(request):
    context = zmq.Context()

    def fin():
        context.destroy()

    request.addfinalizer(fin)
    return context


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


@pytest.mark.timeout(5)
def test_receiver(context, sender_socket, receiver, worker_socket):
    """Receiver should be able to correctly receive messages and send them back"""
    sender_socket.send_multipart([b"test", b"data"])
    data = receiver.recv_data()
    assert data is not None

    time.sleep(1)
    receiver.ventilator.send(data)

    data = worker_socket.recv()
    assert data is not None


@pytest.mark.timeout(5)
def test_receiver_error():
    """Receiver should correctly raise errors"""
    with pytest.raises(TypeError):
        Receiver("127.0.0.1", 6700, output_port=6705, output_socket="/tmp/bad.sock")


@pytest.mark.timeout(5)
def test_receiver_ipc(sender_socket):
    """Receiver should be able to use ipc socket"""
    r = Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")
    time.sleep(1)

    sender_socket.send_multipart([b"test", b"data"])
    data = r.recv_data()
    assert data is not None


def test_receiver_no_args():
    """Receiver should be able to instanciate without output arguments"""
    Receiver("127.0.0.1", 6700)


def test_receiver_log_config():
    """Receiver should be able to use logging configuration file"""
    cf = os.path.join(BASE_DIR, "fixtures/log.cfg")
    Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock", logging_config=cf)


@pytest.mark.timeout(5)
def test_receiver_run(sender_socket):
    """Receiver run method should correctly run and except"""
    r = Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")
    r.ventilator = None

    sender_socket.send_multipart([b"test", b"data"])
    with pytest.raises(AttributeError):
        r.run()
