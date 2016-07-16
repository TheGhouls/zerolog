from zerolog.forwarder import start_forwarder


def run(args):
    """Main run action"""
    start_forwarder(args.frontend, args.backend, args.monitor)


def forwarder_command(sp):
    """Sub parser for forwarder commands"""
    parser = sp.add_parser("forwarder", help="start a forwarder")
    parser.add_argument(
        "-f",
        "--frontend",
        help="frontend port for sending data to receivers",
        type=int,
        default=6001
    )
    parser.add_argument(
        "-b",
        "--backend",
        help="backend port for receiving data",
        type=int,
        default=6000
    )
    parser.add_argument(
        "-m",
        "--monitor",
        help="monitor port for publishing data",
        type=int,
        default=None
    )
    parser.set_defaults(func=run)
