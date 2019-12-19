import logging
import re
import click

from .main import main

_logger = logging.getLogger(__name__)

# from OCA/maintainer-quality-tools
odoo_reg_exp = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \d+ (?P<levelname>\w+) (?P<db>\S+) (?P<logger>\S+): (?P<message>.*)$"

def _parse(stream, reg_exp=odoo_reg_exp):
    for line in stream:
        parsed = re.match(reg_exp,line)
        result = False
        if parsed:
            result = parsed.groupdict()
        yield result


def parseFile(stream, reg_exp=odoo_reg_exp):
    result = []
    for line in _parse(stream, reg_exp):
        if line:
            print(line)
            result.append(line)
    return result

@click.command(
    help="parses an odoo log file and returns a dict for the different part of the log"
)
@click.argument("filename", type=click.Path(dir_okay=False), default="-")
def parse(filename, reg_exp):
    parseFile(filename, reg_exp)


main.add_command(parse)