import time

import zmq
import pytest

from zerolog.worker import BaseWorker


@pytest.fixture(scope='module')
def sender():
    context = zmq.Context()
    s = context.socket(zmq.PUSH)
    s.bind("tcp://*:6800")
    time.sleep(1)
    return s


@pytest.fixture(scope='module')
def worker():
    worker = BaseWorker("tcp://127.0.0.1:6800")
    return worker


def test_base_worker(sender, worker):
    """Base worker should correctly handle data"""
    sender.send(b"test")
    with pytest.raises(NotImplementedError):
        worker.run()
