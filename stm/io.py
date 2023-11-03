import toml
from pathlib import Path
from typing import Union


def open_toml(path: Union[str, Path]) -> dict:
    with open(path) as toml_file:
        data = toml.loads(toml_file.read())
    toml_file.close()
    return data


def save_toml(data: dict, path: Union[str, Path]) -> None:
    with open(path, "w") as toml_file:
        toml_file.write(toml.dumps(data))
    toml_file.close()
