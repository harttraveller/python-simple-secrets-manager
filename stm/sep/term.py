import os
from typing import Any
from rich.console import Console


def vprint(obj: Any, verbose: bool = True) -> None:
    "verbose print utility with rich formatting"
    if verbose:
        Console().print(obj)


def clear():
    "clears terminal output"
    os.system("cls" if os.name == "nt" else "clear")
