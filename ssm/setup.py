import os
from ssm.sep.io import save_toml
from ssm.env import PATH_STORE_DEFAULT, PATH_SECRETS_DEFAULT


def secret_storage(erase: bool = False):
    PATH_STORE_DEFAULT.mkdir(exist_ok=True)
    if erase:
        if PATH_SECRETS_DEFAULT.exists():
            os.remove(PATH_SECRETS_DEFAULT)
    if not PATH_SECRETS_DEFAULT.exists():
        save_toml(dict(), PATH_SECRETS_DEFAULT)
