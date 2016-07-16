"""Reciver module

Contain default receiver. Receiver will be in charge to get data from forwarder
"""
import time
import logging
import logging.config

import zmq


log = logging.getLogger(__name__)


class Receiver:
    """Main receiver class.

    You can use different patterns for receiver and workers :

    * Workers connect to receiver over TCP
    * Workers connect to receiver over ipc protocol (same machine)

    For more flexibility this class allow you to pass an ``output_port`` parameter or
    a ``output_socket``, the last one allowing you to use ``ipc`` protocol between workers and receiver.

    .. warning::

        If both ``output_port`` and ``output_socket`` are set, an error will be raised. If none are
        set, default is to use TCP bind on port 6200

    .. admonition:: Goal of this class

        This class is very basic since there is no specific action here, only data
        data forwarding from forwarder to workers. Yet it's configurable enough to cover
        major use cases, and can be easily override.

        But keep in mind that for large application this class will process a very large amount of data.
        Keep it simple and put logic in workers, there here for that prupose

    :param str forwarder_address: IP or domain of forwarder
    :param int forwarder_port: port to listen for incomming forwarder messages
    :param str topic: publish topic to listen (default to all)
    :param int output_port: port to bind for sending data to workers
    :param str output_socket: location of ipc socket to use for sending data to workers
    :param str logging_config: file path to logging configuration
    :raise: TypeError
    """

    def __init__(self, forwarder_address, forwarder_port, topic=None, *args, **kwargs):

        output_port = kwargs.get("output_port", None)
        output_socket = kwargs.get("output_socket", None)

        if output_port is not None and output_socket is not None:
            raise TypeError("Cannot use both TCP and unix sockets for output")

        self.context = zmq.Context.instance()

        topic = topic or ""
        self.forwarder = self.context.socket(zmq.SUB)
        self.forwarder.setsockopt_string(zmq.SUBSCRIBE, topic)
        self.forwarder.connect("tcp://{}:{}".format(forwarder_address, forwarder_port))

        self.ventilator = self.context.socket(zmq.PUSH)

        output_binding = self.setup_output_socket(output_port, output_socket)
        # sockets warmup
        time.sleep(1)

        if kwargs.get('logging_config') is not None:
            logging.config.fileConfig(kwargs.get('logging_config'))

        log.info("Receiver started")
        log.info("Listening from forwarder on %s:%s", forwarder_address, forwarder_port)
        log.info("Sending data to worker on %s", output_binding)

    def setup_output_socket(self, output_port=None, output_socket=None):
        """Setup PUSH output socket"""
        if output_port is None and output_socket is None:
            output_binding = "tcp://*:6200"
        elif output_socket is None:
            output_binding = "tcp://*:{}".format(output_port)
        else:
            output_binding = "ipc://{}".format(output_socket)

        self.ventilator.bind(output_binding)
        return output_binding

    def recv_data(self):
        """Receive data from forwarder and return them.
        Channel will not be return

        :return: data from forwarder
        :rtype: bytes
        """
        data = self.forwarder.recv_multipart()
        return data[1]

    def run(self):
        """Main receiver loop"""
        try:
            while 1:
                data = self.recv_data()
                self.ventilator.send(data)
        except (Exception, KeyboardInterrupt) as e:
            log.error("Exception occured: %s", e)
            raise
