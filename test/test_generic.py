from ssm import secrets


def test_add():
    secrets.add(name="test-secret", key="test-key")
