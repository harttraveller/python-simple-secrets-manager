import rich_click as click
from stm.handler import tokens
from stm.environment import PKG_VERSION


@click.group(name="stm")
@click.version_option(PKG_VERSION)
@click.pass_context
def entry():
    # todo: cli message
    ...
