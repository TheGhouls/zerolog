"""Base worker implmentation"""
import logging

import zmq


log = logging.getLogger(__name__)


class BaseWorker:
    """Base worker class.

    This class cannot be used "as is", it will raises an ``ImplementationError`` in ``process_data`` methode.
    ``BaseWorker`` provide only a skeleton to help you to develop your own workers

    .. note::
        For conveniance, default recv method for backend socket is ``recv_string()`` from pyzmq.
        But you can change it easily by overloading ``recv_func`` in your worker, for example::

            def __init__(self, backend, *args, **kwargs):
                super(MyWorkerClase, self).__init__(backend, *args, **kwargs)
                self.recv_func = self.backend.recv_json()

    :param str backend: backend zeromq string to connect to receiver. e.g: ``ipc://unix.socket``
    """
    def __init__(self, backend, *args, **kwargs):
        self.context = zmq.Context()
        self.backend = self.context.socket(zmq.PULL)
        self.backend.connect(backend)
        self.recv_func = self.backend.recv_string

    def process_data(self, data):
        """Process data

        :param mixed data: data received from backend
        :raises: NotImplementedError
        """
        raise NotImplementedError("You must override the process data methode")

    def run(self):
        """Main loop for receive messages and process them

        ``self.recv_func`` is used to receive data from backend
        """
        try:
            while 1:
                data = self.recv_func()
                self.process_data(data)
        except (Exception, KeyboardInterrupt) as e:
            log.error("Exception raised : %s", e)
            self.context.destroy()
            raise
