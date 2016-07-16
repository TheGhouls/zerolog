import sys
from unittest.mock import patch

import pytest

from zerolog.commands.main import main
from zerolog.commands.worker import run, get_class


@pytest.fixture
def args():

    class Args:
        backend = "tcp://127.0.0.1:6200"
        worker_class = "zerolog.worker.BaseWorker"
        directory = None

    return Args()


@patch('zerolog.commands.worker.run')
def test_receiver_command(run):
    sys.argv = sys.argv[:1]
    sys.argv += ["worker", "tcp://127.0.0.1:6200", "foo.bar.Class"]
    main()


def test_receiver_get_class():
    c = get_class("zerolog.worker.BaseWorker")
    assert c.__name__ == "BaseWorker"


def test_receiver_run_errors(args):

    args.worker_class = "bad.module"
    with pytest.raises(ImportError):
        run(args)

    args.worker_class = "zerolog.worker.BadClass"
    with pytest.raises(AttributeError):
        run(args)


@patch("zerolog.worker.BaseWorker")
def test_run(base_worker, args):
    run(args)
