from click.testing import CliRunner

from pssm import secrets
from pssm.cli import entry


def test_lib_keep():
    secrets.keep(uid="test-secret", key="test-key")


def test_cli_keep():
    runner = CliRunner()
    # result = runner.invoke(entry)
