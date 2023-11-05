import os
from typing import Any, Union, Optional
from rich.console import Console
from rich.color import ANSI_COLOR_NAMES

# todo: move utils to separate package


def vprint(
    obj: Union[str, Any],
    color: Optional[str] = None,
    prepend_newline: bool = True,
    verbose: bool = True,
) -> None:
    "verbose print utility with rich formatting"
    if verbose:
        if isinstance(obj, str):
            if prepend_newline:
                obj = f"\n{obj}"
            if color is None:
                Console().print(obj)
            else:
                if color in ANSI_COLOR_NAMES.keys():
                    Console().print(f"[{color}]{obj}[/{color}]")
                else:
                    for acn in ANSI_COLOR_NAMES.keys():
                        Console().print(acn)
                    raise ValueError(
                        f"argument passed to 'color' must be one of the colors listed above"
                    )
        else:
            Console().print(obj)


def clear():
    "clears terminal output"
    os.system("cls" if os.name == "nt" else "clear")
