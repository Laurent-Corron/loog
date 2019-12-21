import re
from typing import Iterable, Iterator, MutableMapping

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


def parse_stream(stream: Iterable[str]) -> Iterator[MutableMapping[str, str]]:
    """Parse a stream of Odoo log lines and return an iterator of log records.

    Log records have the following keys:
    - asctime: timestamp
    - pid: process or thread id
    - dbname: database name
    - logger: python logger name
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
    if record:
        yield record


ODOO_WERKZEUG_RE = re.compile(
    r"^(?P<remote_addr>\S+)"
    r" .+? .+? \[.*?\]"
    r" \"(?P<request_method>\S+) (?P<request_uri>\S+) .*?\""
    r" (?P<status>\S+) \S+"
    r"( (?P<perf_info>"
    r"(?P<sql_count>\d+) "
    r"(?P<sql_time>\d*\.\d+) "
    r"(?P<python_time>\d*\.\d+)"
    r"))?"
    r".*$"
)


def enrich_werkzeug(
    records: Iterable[MutableMapping[str, str]]
) -> Iterator[MutableMapping[str, str]]:
    """Enrich werkzeug (http requests) log records"""
    for record in records:
        if record.get("logger") == "werkzeug":
            mo = ODOO_WERKZEUG_RE.match(record["message"])
            if mo:
                record.update(
                    (k, v) for k, v in mo.groupdict().items() if v is not None
                )
        yield record
