import re
from typing import Iterable, Iterator, MutableMapping
from urllib.parse import urlparse

# from tartley/colorama
ANSI_CSI_RE = re.compile("\001?\033\\[((?:\\d|;)*)([a-zA-Z])\002?")

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


def parse_stream(
    stream: Iterable[str], include_raw: bool = False
) -> Iterator[MutableMapping[str, str]]:
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
        line = ANSI_CSI_RE.sub("", line)
        mo = ODOO_LOG_RE.match(line)
        if mo:
            # we got a match, yield previous record and create a new one
            if record:
                yield record
            record = mo.groupdict()
            if include_raw:
                record["raw"] = line
        else:
            if record:
                # irregular line in the middle of the log file: assume
                # it is a continuation of the current record (a typical
                # example is a multi-line stack trace)
                record["message"] += "\n" + line.strip()
                if include_raw:
                    record["raw"] += line
            else:
                # irregular lines at the beginning, yield them independently
                r = {"message": line.strip()}
                if include_raw:
                    r["raw"] = line
                yield r
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
    r"(?P<other_time>\d*\.\d+)"
    r"))?"
    r".*$"
)


def _convert_field(d, k, converter):
    if k in d:
        try:
            d[k] = converter(d[k])
        except Exception:
            del d[k]


def enrich_werkzeug(
    records: Iterable[MutableMapping[str, str]]
) -> Iterator[MutableMapping[str, str]]:
    """Enrich werkzeug (http requests) log records"""
    for record in records:
        if record.get("logger") == "werkzeug":
            mo = ODOO_WERKZEUG_RE.match(record.get("message", ""))
            if mo:
                record.update(
                    (k, v) for k, v in mo.groupdict().items() if v is not None
                )
                record["request_path"] = urlparse(record["request_uri"]).path
                _convert_field(record, "sql_count", int)
                _convert_field(record, "sql_time", float)
                _convert_field(record, "other_time", float)
                if "sql_time" in record and "other_time" in record:
                    record["total_time"] = record["sql_time"] + record["other_time"]
        yield record


def enrich(
    records: Iterable[MutableMapping[str, str]]
) -> Iterator[MutableMapping[str, str]]:
    return enrich_werkzeug(records)
