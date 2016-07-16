import logging

import zmq

log = logging.getLogger(__name__)


def start_forwarder(pub_port, receive_port, mon_port=None):
    """Start a zeromq proxy for forwarding messages from TCP socket to zmq PUB socket

    :param int pub_port: port number to use for publishing messages to workers
    :param int receive_port: port number to use for receiving messages
    :param int mon_port (optional): port to use for monitor socket
    """
    context = zmq.Context()

    frontend = context.socket(zmq.PUB)
    frontend.bind("tcp://*:{}".format(pub_port))

    backend = context.socket(zmq.STREAM)
    backend.bind("tcp://*:{}".format(receive_port))

    if mon_port is not None:
        monitor = context.socket(zmq.PUB)
        monitor.bind("tcp://*:{}".format(mon_port))

        log.info("Starting forwarder")
        log.info("frontend: {}\tbackend: {}\tmonitor: {}".format(pub_port, receive_port, mon_port))

        zmq.proxy(frontend, backend, monitor)
    else:
        log.info("Starting forwarder")
        log.info("frontend: {}\tbackend: {}".format(pub_port, receive_port))
        zmq.proxy(frontend, backend)
