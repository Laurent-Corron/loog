# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import click
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("loog").version
except DistributionNotFound:
    # package is not installed
    pass

__notice__ = """%(prog)s, version %(version)s

An Odoo log parsing and enrichment library and CLI.

Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)"""


@click.group()
@click.version_option(version=__version__, message=__notice__)
@click.pass_context
def main(ctx):
    print()
