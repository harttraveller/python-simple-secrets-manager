import os
from typing import Any, Union, Optional
from rich.console import Console
from rich.color import ANSI_COLOR_NAMES

# todo: move utils to separate package


def vprint(
    obj: Union[str, Any],
    color: Optional[str] = None,
    pn: bool = False,
    verbose: bool = True,
) -> None:
    """
    verbose print utility with rich formatting

    Args:
        obj (Union[str, Any]): object to print
        color (Optional[str], optional): color of string if string. Defaults to None.
        pn (bool, optional): prepend newline if string. Defaults to False.
        verbose (bool, optional): print object. Defaults to True.

    Raises:
        ValueError: invalid color
    """
    if verbose:
        if isinstance(obj, str):
            if pn:
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
