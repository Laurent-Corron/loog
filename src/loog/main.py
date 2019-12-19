# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)

import logging

import click
import io

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("loog").version
except DistributionNotFound:
    # package is not installed
    pass

__notice__ = """%(prog)s, version %(version)s

A logger for Odoo.

Copyright 2019-2020 ACSONE SA/NV (<http://acsone.eu>)"""

@click.group()
@click.version_option(version=__version__, message=__notice__)

@click.pass_context
def main(ctx):
    print()
