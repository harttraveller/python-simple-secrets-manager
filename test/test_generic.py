from ssm import secrets


def test_add():
    secrets.keep(name="test-secret", key="test-key")
