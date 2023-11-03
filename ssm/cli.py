import rich_click as click
from rich.table import Table
from pick import pick
from loguru import logger as log
from typing import Optional
from ssm.core import tokens, TokenHandler
from ssm.sep.term import vprint
from ssm.sep.system import to_clipboard
from ssm.env import PKG_VERSION


def warn(msg: str, crit: bool = False) -> None:
    if crit:
        log.critical(msg)
    else:
        vprint(msg, color="red")


def partial_hide_secret(secret: str):
    quarter_secret = int(len(secret) / 4)
    third_secret = len(secret) - quarter_secret
    hidden = "*" * third_secret
    return f"{secret[:quarter_secret]}{hidden}"


def display_token_table(tokens: TokenHandler):
    table = Table(title="Simple Token Manager: Saved Tokens", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Secret", justify="left", style="magenta", no_wrap=True)
    for token_name, token_data in tokens.data.items():
        table.add_row(token_name, partial_hide_secret(token_data["secret"]))
    vprint(table)


@click.group(name="tokens", invoke_without_command=True)
@click.version_option(PKG_VERSION)
@click.pass_context
def entry(ctx):
    # todo: cli message
    if ctx.invoked_subcommand is None:
        ctx.invoke(tokens_show)


@entry.command(name="show", help="Show a table of tokens.")
def tokens_show():
    display_token_table(tokens)


@entry.command(name="names", help="View the names of the saved tokens.")
def tokens_names():
    for name in tokens.names:
        vprint(name)


@entry.command(name="view", help="View a secret for a token.")
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=False,
    required=True,
)
@click.option(
    "--name",
    "-n",
    type=str,
    default=None,
    help="Name of API token.",
    required=True,
)
def tokens_view(interactive: bool, name: Optional[str]):
    pass
    # if (name is None) and (not interactive):
    #     vprint(
    #         "\nYou must enter a token name (-n) or use interactive mode (-i).",
    #         color="red",
    #     )


@entry.command(name="copy")
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=False,
    required=True,
)
def tokens_copy():
    pass


# todo: add secure input mode
@entry.command(name="save")
@click.option(
    "--secure/--unsafe",
    "-s/-u",
    type=bool,
    default=True,
    required=True,
    help="Secure input (interactive) mode, requires terminal access.",
)
def tokens_save(secure: bool):
    if secure:
        pass
    else:
        warn(
            "Passing a token as an argument will leave it in your terminal history, and is not recommended."
        )


@entry.command(name="del")
def tokens_delete():
    # api_token = tokens.get(selection[0])
    # subprocess.run("pbcopy", text=True, input=api_token)
    # vprint(f"[green]{selection[0].title()} Token Copied[/green]")
    ...
