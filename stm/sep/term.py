import os
from typing import Any, Union
from rich.console import Console
from rich.color import ANSI_COLOR_NAMES

# todo: move utils to separate package


def vprint(obj: Union[str, Any], verbose: bool = True) -> None:
    "verbose print utility with rich formatting"
    if verbose:
        Console().print(obj)


def clear():
    "clears terminal output"
    os.system("cls" if os.name == "nt" else "clear")
