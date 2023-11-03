import rich_click as click
from stm.handler import tokens
from stm.environment import PKG_VERSION


@click.group(name="tokens")
@click.version_option(PKG_VERSION)
@click.pass_context
def entry():
    # todo: cli message
    ...


@entry.command(name="list")
def tokens_list():
    pass


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
