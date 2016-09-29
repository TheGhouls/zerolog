import logging

import zmq

log = logging.getLogger(__name__)


def start_forwarder(pub_port, receive_port, mon_port=None, backend_socket=None, frontend_socket=None):
    """Start a zeromq proxy for forwarding messages from TCP socket to zmq PUB socket

    :param int pub_port: port number to use for publishing messages to workers
    :param int receive_port: port number to use for receiving messages
    :param int mon_port (optional): port to use for monitor socket
    :param str backend_socket (optionnal): socket type to use for backend socket
    :param str frontend_socket (optionnal): socket type to use for frontend socket
    """
    context = zmq.Context()

    if frontend_socket is not None:
        try:
            frontend_socket = getattr(zmq, frontend_socket.upper())
        except AttributeError:
            frontend_socket = zmq.PUB
            log.warning("Bad frontend type provided :{}\nForwarder will use default PUB type".format(frontend_socket))
    else:
        frontend_socket = zmq.PUB

    frontend = context.socket(frontend_socket)
    frontend.bind("tcp://*:{}".format(pub_port))

    if backend_socket is not None:
        try:
            backend_socket = getattr(zmq, backend_socket.upper())
        except AttributeError:
            backend_socket = zmq.STREAM
            log.warning("Bad backend type provided :{}\nForwarder will use default STREAM type".format(backend_socket))
    else:
        backend_socket = zmq.STREAM

    backend = context.socket(backend_socket)
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
