"""Base worker implmentation"""
import logging

import zmq


log = logging.getLogger(__name__)


class BaseWorker:
    """Base worker class.

    :param str backend: backend zeromq string to connect to receiver. e.g: ``ipc://unix.socket``
    """
    def __init__(self, backend, *args, **kwargs):
        self.context = zmq.Context()
        self.backend = self.context.socket(zmq.PULL)
        self.backend.connect(backend)

    def process_data(self, data):
        """Process data received from backend

        :param mixed data: data received from backend
        """
        raise NotImplementedError("You must override the process data methode")

    def run(self):
        try:
            while 1:
                data = self.backend.recv()
                self.process_data(data)
        except (Exception, KeyboardInterrupt) as e:
            log.error("Exception raised : %s", e)
            self.context.destroy()
            raise
