"""Reciver module

Contain default receiver. Receiver will be in charge to get data from forwarder
"""
import zmq


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
    :raise: TypeError
    """

    def __init__(self, forwarder_address, forwarder_port, topic=None):
        pass


    def setup_output_socket(self, output_port=None, output_socket=None):
        """Setup PUSH output socket"""

    def recv_data(self):
        """Receive data from forwarder and return them.
        Channel will not be return

        :return: data from forwarder
        :rtype: bytes
        """
        pass

    def process(self, data):
        """Process data and send them to workers"""
        pass

