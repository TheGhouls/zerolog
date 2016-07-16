import logging
import importlib

log = logging.getLogger(__name__)


def get_class(kls):
    parts = kls.split('.')
    mod_name = ".".join(parts[:-1])
    mod = importlib.import_module(mod_name)
    kls = getattr(mod, parts[-1])
    return kls


def run(args):
    """Main worker run command"""
    try:
        kls = get_class(args.worker_class)
        worker = kls(args.backend)
        worker.run()
    except ImportError:
        log.error("Bad module provided for worker class")
        return
    except AttributeError:
        log.error("Class not found")
        return


def worker_command(sp):
    """Sub parser for worker commands"""
    parser = sp.add_parser("worker", help="start a worker")

    parser.add_argument(
        "backend",
        help="backend to connect for receiving message (e.g: tcp://127.0.0.1:6200)"
    )
    parser.add_argument(
        "worker_class",
        help="class to use as worker"
    )

    parser.set_defaults(func=run)