import rich_click as click
from pick import pick
from stm.handler import tokens
from stm.sep.term import vprint
from stm.environment import PKG_VERSION


@click.group(name="tokens")
@click.version_option(PKG_VERSION)
@click.pass_context
def entry():
    # todo: cli message
    ...


@entry.command(name="names", help="View the names of the saved tokens.")
def tokens_names():
    for name in tokens.names:
        vprint(name)


@entry.command(name="view")
def tokens_view():
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
