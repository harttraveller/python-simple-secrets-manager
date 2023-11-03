import os
from ssm.sep.io import save_toml
from ssm.env import PATH_STORE_DEFAULT, PATH_TOKENS_DEFAULT


def token_storage(erase: bool = False):
    PATH_STORE_DEFAULT.mkdir(exist_ok=True)

    if erase:
        if PATH_TOKENS_DEFAULT.exists():
            os.remove(PATH_TOKENS_DEFAULT)
    if not PATH_TOKENS_DEFAULT.exists():
        save_toml(dict(), PATH_TOKENS_DEFAULT)
