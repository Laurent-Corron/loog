# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import json
import sys

import click

from .parser import enrich, enrich_errors, parse_stream

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
    for record in enrich(parse_stream(sys.stdin)):
        json.dump(record, sys.stdout)
        sys.stdout.write("\n")


@click.command()
@click.option(
    "--ignore",
    "-i",
    metavar="REGEX",
    multiple=True,
    help="Regular expression for message to ignore (can be repeated).",
)
def check(ignore):
    for record in enrich_errors(parse_stream(sys.stdin), regexes_to_ignore=ignore):
        json.dump(record, sys.stdout)
        sys.stdout.write("\n")


main.add_command(check)
