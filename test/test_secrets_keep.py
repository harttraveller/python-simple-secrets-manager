from click.testing import CliRunner

from ssm import secrets
from ssm.cli import entry


def test_lib_keep():
    secrets.keep(name="test-secret", key="test-key")


def test_cli_keep():
    runner = CliRunner()
    # result = runner.invoke(entry)
