# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import click

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("loog")

__notice__ = """%(prog)s, version %(version)s

An Odoo log parsing and enrichment library and CLI.

Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)"""


@click.group()
@click.version_option(version=__version__, message=__notice__)
def main() -> None:
    print()
