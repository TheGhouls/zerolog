import sys
from unittest.mock import patch

from zerolog.commands.main import main


@patch('zerolog.commands.receiver.Receiver')
def test_receiver_command(receiver):
    sys.argv = sys.argv[:1]
    sys.argv += ["receiver", "127.0.0.1", "6001"]
    main()
    sys.argv = sys.argv[:1]
