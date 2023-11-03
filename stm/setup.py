from pathlib import Path
from stm.sep.io import save_toml
from stm.env import PATH_STORE_DEFAULT, PATH_TOKENS_DEFAULT

PATH_STORE_DEFAULT.mkdir(exist_ok=True)

if not PATH_TOKENS_DEFAULT.exists():
    save_toml(PATH_TOKENS_DEFAULT, dict())
