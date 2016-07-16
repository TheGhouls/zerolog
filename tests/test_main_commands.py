import pytest
from unittest.mock import patch

from zerolog.commands.main import main


def test_main_error():
    with pytest.raises(SystemExit):
        main()


@patch("zerolog.commands.main.argparse.ArgumentParser.parse_args")
def test_main(parse_args):
    main()
