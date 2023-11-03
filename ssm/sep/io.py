import toml
from pathlib import Path
from typing import Union

# todo: replace with pyeio and integrate there


def open_toml(path: Union[str, Path]) -> dict:
    "Open a toml file."
    with open(path) as toml_file:
        data = toml.loads(toml_file.read())
    toml_file.close()
    return data


def save_toml(data: dict, path: Union[str, Path]) -> None:
    "Save data to toml file."
    with open(path, "w") as toml_file:
        toml_file.write(toml.dumps(data))
    toml_file.close()
