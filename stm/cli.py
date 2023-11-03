import rich_click as click
from rich.table import Table
from pick import pick
from typing import Optional
from stm.core import tokens, TokenHandler
from stm.sep.term import vprint
from stm.env import PKG_VERSION


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


@entry.command(name="view")
@click.option(
    "--name",
    "-n",
    type=str,
    help="Name of API token.",
    required=False,
)
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=False,
    required=True,
)
def tokens_view(name: Optional[str], interactive: bool):
    pass


@entry.command(name="copy")
def tokens_copy():
    pass


@entry.command(name="save")
def tokens_save():
    pass


@entry.command(name="del")
def tokens_delete():
    pass
