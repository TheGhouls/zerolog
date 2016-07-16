from zerolog.receiver import Receiver


def run(args):
    """Run receiver"""
    kwargs = vars(args)

    forwarder_address = kwargs.pop('forwarder_address')
    forwarder_port = kwargs.pop('forwarder_port')
    topic = kwargs.pop('topic')

    receiver = Receiver(forwarder_address, forwarder_port, topic, **kwargs)
    receiver.run()


def receiver_command(sp):
    """Receiver subparser"""
    parser = sp.add_parser("receiver", help="receiver sub commands")

    parser.add_argument(
        'forwarder_address',
        help="address of running forwarder"
    )
    parser.add_argument(
        'forwarder_port',
        type=int,
        help="port of running forwarder"
    )
    parser.add_argument(
        '-t',
        '--topic',
        help="optional topic to subscribe",
        default=None
    )
    parser.add_argument(
        '-l',
        '--log-config',
        help="location of logging configuration file (python standard logging configuration file)"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--output-port',
        type=int,
        help="output TCP port for workers (default to 6200)"
    )
    group.add_argument(
        '--output-socket',
        help="output unix socket for workers"
    )

    parser.set_defaults(func=run)
