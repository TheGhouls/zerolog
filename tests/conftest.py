import zmq
import pytest


@pytest.fixture(scope='module')
def context():
    return zmq.Context()
