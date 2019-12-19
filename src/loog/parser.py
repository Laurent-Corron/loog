import re
from typing import Iterable, Iterator, Mapping


ODOO_LOG_RE = re.compile(
    r"^"
    r"(?P<asctime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) "
    r"(?P<pid>\d+) "
    r"(?P<levelname>\w+) "
    r"(?P<dbname>\S+) "
    r"(?P<logger>\S+): "
    r"(?P<message>.*)"
    r"$"
)

def parse_stream(stream: Iterable[str]) -> Iterator[Mapping[str, str]]:
    """Parse a stream of Odoo log lines and return an iterator of log records.

    Log records have the following keys:
    - asctime: timestamp
    - pid: process or thread id
    - dbname: database name
    - levelname: python logging level name
    - message: the rest of the line
    """
    record = None
    for line in stream:
        mo = ODOO_LOG_RE.match(line)
        if mo:
            # we got a match, yield previous record and create a new one
            if record:
                yield record
            record = mo.groupdict()
            record["raw"] = line
        else:
            if record:
                # irregular line in the middle of the log file: assume
                # it is a continuation of the current record (a typical
                # example is a multi-line stack trace)
                record["message"] += "\n" + line.strip()
                record["raw"] += line
            else:
                # irregular lines at the beginning, yield them independently
                yield {"raw": line}

if __name__ == "__main__":
    import sys
