import os
import time

import zmq
import pytest

from zerolog.receiver import Receiver

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='module')
def context(request):
    context = zmq.Context()
    return context


@pytest.fixture(scope='module')
def sender_socket(context):
    s = context.socket(zmq.PUB)
    s.setsockopt(zmq.LINGER, 0)
    s.bind("tcp://*:6700")
    time.sleep(1)
    return s


@pytest.fixture(scope='module')
def worker_socket(context):
    s = context.socket(zmq.PULL)
    s.setsockopt(zmq.LINGER, 0)
    s.connect("tcp://127.0.0.1:6705")
    return s


@pytest.fixture(scope='module')
def receiver():
    r = Receiver("127.0.0.1", 6700, output_port=6705)
    r.forwarder.setsockopt(zmq.LINGER, 0)
    r.ventilator.setsockopt(zmq.LINGER, 0)
    return r


@pytest.mark.timeout(10)
def test_receiver(context, sender_socket, receiver, worker_socket):
    """Receiver should be able to correctly receive messages and send them back"""
    for i in range(10):
        sender_socket.send_multipart([b"", b"data"])
    data = receiver.recv_data()
    assert data is not None

    receiver.ventilator.send(data)

    data = worker_socket.recv()
    assert data is not None


@pytest.mark.timeout(5)
def test_receiver_error():
    """Receiver should correctly raise errors"""
    with pytest.raises(TypeError):
        Receiver("127.0.0.1", 6700, output_port=0, output_socket="bad.sock")


@pytest.mark.timeout(5)
def test_receiver_ipc(sender_socket):
    """Receiver should be able to use ipc socket"""
    r = Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")
    r.forwarder.setsockopt(zmq.LINGER, 0)
    r.ventilator.setsockopt(zmq.LINGER, 0)

    for i in range(10):
        sender_socket.send_multipart([b"test", b"data"])
    data = r.recv_data()
    assert data is not None


def test_receiver_no_args():
    """Receiver should be able to instanciate without output arguments"""
    r = Receiver("127.0.0.1", 6700)
    r.forwarder.setsockopt(zmq.LINGER, 0)
    r.context.destroy()


def test_receiver_log_config():
    """Receiver should be able to use logging configuration file"""
    cf = os.path.join(BASE_DIR, "fixtures/log.cfg")
    r = Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock", logging_config=cf)
    r.forwarder.setsockopt(zmq.LINGER, 0)


@pytest.mark.timeout(5)
def test_receiver_run(sender_socket):
    """Receiver run method should correctly run and except"""
    r = Receiver("127.0.0.1", 6700, output_socket="/tmp/test.sock")
    r.forwarder.setsockopt(zmq.LINGER, 0)
    r.ventilator = None

    sender_socket.send_multipart([b"test", b"data"])
    with pytest.raises(AttributeError):
        r.run()
