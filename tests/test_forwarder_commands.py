import sys
from unittest.mock import patch

from zerolog.commands.main import main


@patch("zerolog.commands.forwarder.start_forwarder")
def test_forwarder_cli(start_forwarder):
    """we should be able to start forwarder from cli"""
    sys.argv = sys.argv[:1]
    sys.argv += ["forwarder"]
    main()
    sys.argv = sys.argv[:1]
