# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import json
import sys

import click

from .config import LoogConfig
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
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False, exists=True),
    help="Configuration file (default: ./loog.cfg).",
)
@click.pass_context
def main(ctx, config):
    config = LoogConfig(config)

    ctx.obj = dict(config=config)
    ctx.default_map = config.get_default_map()


@click.command()
def parse() -> None:
    for record in enrich(parse_stream(sys.stdin)):
        json.dump(record, sys.stdout)
        sys.stdout.write("\n")


main.add_command(parse)


@click.command()
@click.option(
    "--ignore",
    "-i",
    metavar="REGEX",
    multiple=True,
    help="Regular expression for message to ignore (can be repeated).",
)
@click.option(
    "--human-readable",
    "-h",
    is_flag=True,
    help="shows a clear list of errors that weren't ignored by -i",
)
@click.option(
    "--err-if-err",
    "-e",
    is_flag=True,
    help="Exit with an error code if an error in the log records is found (default).",
)
def check(ignore, human_readable, err_if_err):
    for record in enrich_errors(
        parse_stream(sys.stdin, include_raw=True), regexes_to_ignore=ignore
    ):
        if record["error"]:
            if human_readable:
                click.echo(record["raw"])
            else:
                json.dump(record, sys.stdout)
            sys.stdout.write("\n")
            if err_if_err and not record["error_ignored"]:
                raise click.ClickException("an error was found")


main.add_command(check)


def _read_defaults_check(config):
    section = "check"
    defaults = dict(
        ignore=config.getlist(section, "ignore", []),
        err_if_err=config.getboolean(section, "err-if-err", False),
        human_readable=config.getboolean(section, "human-readable", False),
    )
    return dict(check=defaults)


LoogConfig.add_default_map_reader(_read_defaults_check)
