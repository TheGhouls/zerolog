import zmq


def start_forwarder(pub_port, receive_port, mon_port=None):
    """Start a zeromq proxy for forwarding messages from TCP socket to zmq PUB socket

    :param str pub_port: port number to use for publishing messages to workers
    :param str receive_port: port number to use for receiving messages
    :pram str mon_port (optional): port to use for monitor socket
    """
    context = zmq.Context()

    frontend = context.socket(zmq.PUB)
    frontend.bind("tcp://*:{}".format(pub_port))

    backend = context.socket(zmq.STREAM)
    backend.bind("tcp://*:{}".format(receive_port))

    if mon_port is not None:
        monitor = context.socket(zmq.PUB)
        monitor.bind("tcp://*:{}".format(mon_port))
        zmq.proxy(frontend, backend, monitor)
    else:
        zmq.proxy(frontend, backend)
