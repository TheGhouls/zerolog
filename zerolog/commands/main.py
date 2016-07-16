import argparse

from zerolog.commands.forwarder import forwarder_command
from zerolog.commands.receiver import receiver_command
from zerolog.commands.worker import worker_command


PARSERS = [
    forwarder_command,
    receiver_command,
    worker_command
]


def build_parser():
    parser = argparse.ArgumentParser(prog='zerolog')
    subparsers = parser.add_subparsers(help='sub commands avaibles', dest='parser')
    subparsers.required = True

    for p in PARSERS:
        p(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
