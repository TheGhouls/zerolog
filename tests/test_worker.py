import time

import zmq
import pytest

from zerolog.worker import BaseWorker


@pytest.fixture
def context(request):
    context = zmq.Context()

    def fin():
        context.destroy()

    request.addfinalizer(fin)
    return context


@pytest.fixture
def sender(context):
    s = context.socket(zmq.PUSH)
    s.bind("tcp://*:6800")
    return s


@pytest.fixture
def worker(context):
    worker = BaseWorker("tcp://127.0.0.1:6800")
    return worker


@pytest.mark.timeout(5)
def test_base_worker(sender, worker):
    """Base worker should correctly handle data"""
    sender.send(b"test")
    with pytest.raises(NotImplementedError):
        worker.run()
