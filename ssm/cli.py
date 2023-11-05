import rich_click as click
from rich.table import Table
from pick import pick
from loguru import logger as log
from typing import Optional
from ssm.core import secrets, SecretHandler
from ssm.sep.term import vprint
from ssm.sep.system import to_clipboard
from ssm.env import PACKAGE_NAME, PACKAGE_VERSION


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


def display_token_table(secrets: SecretHandler):
    table = Table(title="Simple Secret Manager Secrets", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Secret", justify="left", style="magenta", no_wrap=True)
    for token_name, token_data in secrets.data.items():
        table.add_row(token_name, partial_hide_secret(token_data["secret"]))
    vprint(table)


@click.group(invoke_without_command=True)
@click.version_option(PACKAGE_VERSION, prog_name=PACKAGE_NAME)
@click.pass_context
def entry(ctx):
    # todo: cli message
    if ctx.invoked_subcommand is None:
        ctx.invoke(secrets_wizard)


# todo: add secure input mode
@entry.command(name="keep", help="Keep (ie: save) a new secret.")
@click.option(
    "--secure/--no-secure",
    "-s/-ns",
    type=bool,
    default=True,
    required=True,
    help="secure input (interactive) mode, requires terminal access",
)
@click.option(
    "--overwrite/--no-overwrite",
    "-o/-no",
    type=bool,
    default=False,
    required=True,
    help="if a secret with the same name exists, overwrite it",
)
@click.option(
    "--name",
    "-n",
    type=str,
    required=False,
    help="the name of the secret to save",
)
@click.option(
    "--key",
    "-k",
    type=str,
    required=False,
    help="the secret key to save",
)
# todo: overwrite option
def secrets_keep(secure: bool):
    if secure:
        pass
    else:
        warn(
            "Passing a token as an argument will leave it in your terminal history, and is not recommended."
        )


# todo: command.security - review revolving, checks
# todo: command.peek
# todo: keep


@entry.command(name="wizard", help="Secrets CLI wizard.")
def secrets_wizard():
    pass


@entry.command(name="list", help="List secrets in a table.")
# @click.option("--sort")
# @click.option("--filter") *regex
def secrets_table():
    if secrets.count():
        display_token_table(secrets)
        # for name in secrets.names:
        #     vprint(name)
    else:
        vprint("You haven't saved any secrets yet...", color="yellow")


@entry.command(name="find", help="View the names of the saved secrets.")
def secrets_find():
    pass


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
def secrets_view(interactive: bool, name: Optional[str]):
    pass
    # if (name is None) and (not interactive):
    #     vprint(
    #         "\nYou must enter a token name (-n) or use interactive mode (-i).",
    #         color="red",
    #     )


@entry.command(name="copy", help="Copy a secret key to your clipboard.")
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=False,
    required=True,
)
def secrets_copy():
    pass


@entry.command(name="edit", help="Edit an existing secret.")
def secrets_edit():
    pass


@entry.command(name="forget", help="Forget (ie: delete) a secret.")
def secrets_forget():
    # api_token = secrets.get(selection[0])
    # subprocess.run("pbcopy", text=True, input=api_token)
    # vprint(f"[green]{selection[0].title()} Token Copied[/green]")
    ...


# @entry.command(name="config", help="Configuration.")
