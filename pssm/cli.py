import rich_click as click
from rich.table import Table
from pick import pick
from getpass import getpass
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


def display_secret_table(secrets: SecretHandler):
    table = Table(title="Secrets", min_width=80)
    table.add_column("UID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Key", justify="left", style="magenta", no_wrap=True)
    for secret_name, secret_data in secrets.data.items():
        table.add_row(secret_name, partial_hide_secret(secret_data["key"]))
    vprint(table)


@click.group(invoke_without_command=True)
@click.version_option(PACKAGE_VERSION, prog_name=PACKAGE_NAME)
@click.pass_context
def entry(ctx):
    # todo: cli message
    pass
    # if ctx.invoked_subcommand is None:
    #     ctx.invoke(secrets_wizard)


# todo: add secure input mode
@entry.command(name="keep", help="Keep (ie: save) a new secret.")
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=True,
    required=True,
    help="Interactive mode or arguments mode.",
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
    "--uid",
    "-u",
    type=str,
    required=False,
    help="the uid of the secret to save",
)
@click.option(
    "--key",
    "-k",
    type=str,
    required=False,
    help="the secret key to save",
)
# todo: overwrite option
def secrets_keep(
    interactive: bool,
    overwrite: bool,
    uid: Optional[str] = None,
    key: Optional[str] = None,
):
    # todo: implement overwrite block if necessary
    remember_message = lambda: vprint("Secret remembered!", color="light_green")
    if interactive:
        if (uid is not None) or (key is not None):
            vprint("Passing arguments is disabled in interactive mode.", color="yellow")
        else:
            secret_uid = str(input("uid ❯ "))
            secret_key = getpass("key ❯ ")
            try:
                secrets.keep(uid=secret_uid, key=secret_key)
                remember_message()
            except ValueError as exc:
                vprint(str(exc), color="red")
    else:
        if uid is None:
            vprint("Secret uid (-u) must be passed.", color="yellow")
        elif key is None:
            vprint("Secret key (-k) must be passed.", color="yellow")
        else:
            vprint(
                "Using arguments mode leaves secret keys in your terminal history and accordingly it is not recommended.",
                color="red",
            )
            try:
                secrets.keep(uid=uid, key=key)
                remember_message()
            except ValueError as exc:
                vprint(str(exc), color="red")

        # if name exists and not overwrite, block
        # else, save secret


@entry.command(name="list", help="List secrets in a table.")
# @click.option("--sort")
# @click.option("--filter") *regex
def secrets_list():
    if secrets.count():
        display_secret_table(secrets)
        # for name in secrets.names:
        #     vprint(name)
    else:
        vprint("You haven't saved any secrets yet...", color="yellow")


@entry.command(name="forget", help="Forget (ie: delete) a secret.")
@click.option(
    "--interactive/--arguments",
    "-i/-a",
    type=bool,
    default=True,
    required=True,
    help="Interactive mode or arguments.",
)
@click.option(
    "--uid",
    "-u",
    type=str,
    required=False,
    default=None,
    help="Pass a secrets uid to forget it.",
)
def secrets_forget(interactive: bool, uid: Optional[str]):
    if not secrets.count():
        vprint("No secrets to forget yet.", color="yellow")
    else:
        if interactive:
            title = "Select (spacebar) secret(s), and hit enter to forget."
            options = secrets.uids
            selected = pick(options, title, multiselect=True)
        else:
            if uid is None:
                vprint(
                    "If you are not using interactive mode, you must pass a secret uid.",
                    color="yellow",
                )
            else:
                if not secrets.exists(uid):
                    vprint(
                        "Can't seem to find that secret... Make sure that uid exists. (Hint: run 'secrets list' to check).",
                        color="yellow",
                    )
                else:
                    secrets.forget(uid=uid)
                    vprint("Secret forgotten!", color="light_green")


# todo: command.security - review revolving, checks
# todo: command.peek
# todo: keep


# @entry.command(name="wizard", help="Secrets CLI wizard.")
# def secrets_wizard():
#     pass


# @entry.command(name="find", help="View the names of the saved secrets.")
# def secrets_find():
#     pass


# @entry.command(name="view", help="View a secret for a token.")
# @click.option(
#     "--interactive/--arguments",
#     "-i/-a",
#     type=bool,
#     default=False,
#     required=True,
# )
# @click.option(
#     "--name",
#     "-n",
#     type=str,
#     default=None,
#     help="Name of API token.",
#     required=True,
# )
# def secrets_view(interactive: bool, name: Optional[str]):
#     pass
#     # if (name is None) and (not interactive):
#     #     vprint(
#     #         "\nYou must enter a token name (-n) or use interactive mode (-i).",
#     #         color="red",
#     #     )


# @entry.command(name="copy", help="Copy a secret key to your clipboard.")
# @click.option(
#     "--interactive/--arguments",
#     "-i/-a",
#     type=bool,
#     default=False,
#     required=True,
# )
# def secrets_copy():
# api_token = secrets.get(selection[0])
# subprocess.run("pbcopy", text=True, input=api_token)
# vprint(f"[green]{selection[0].title()} Token Copied[/green]")


# @entry.command(name="edit", help="Edit an existing secret.")
# def secrets_edit():
#     pass


# # @entry.command(name="config", help="Configuration.")
