# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import json
import os

from loog import enrich_errors, enrich_werkzeug, parse_stream

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_empty():
    path = os.path.join(DATA_DIR, "empty.log")
    with open(path) as file:
        assert list(parse_stream(file)) == []


def test_parsing_file():
    path = os.path.join(DATA_DIR, "test1.log")
    with open(path) as file:
        result = list(parse_stream(file, include_raw=True))
    with open(os.path.join(DATA_DIR, "test1_expected.json")) as expected_file:
        expected = json.load(expected_file)
    assert expected == result


def test_ansi():
    path = os.path.join(DATA_DIR, "test_ansi.log")
    with open(path) as file:
        result = list(parse_stream(file, include_raw=False))
    with open(os.path.join(DATA_DIR, "test_ansi_expected.json")) as expected_file:
        expected = json.load(expected_file)
    assert expected == result


def test_include_raw():
    path = os.path.join(DATA_DIR, "test1.log")
    with open(path) as file:
        assert all("raw" in r for r in parse_stream(file, include_raw=True))
    with open(path) as file:
        assert all("raw" not in r for r in parse_stream(file, include_raw=False))
    with open(path) as file:
        assert all("raw" not in r for r in parse_stream(file))


def test_werkzeug():
    path = os.path.join(DATA_DIR, "test_werkzeug.log")
    with open(path) as file:
        result = list(enrich_werkzeug(parse_stream(file)))
    with open(os.path.join(DATA_DIR, "test_werkzeug_expected.json")) as expected_file:
        expected = json.load(expected_file)
    assert expected == result


def test_enrich_errors():
    path = os.path.join(DATA_DIR, "test_error.log")
    with open(path) as file:
        result = list(enrich_errors(parse_stream(file, include_raw=True)))
    with open(os.path.join(DATA_DIR, "test_error_expected.json")) as expected_file:
        expected = json.load(expected_file)
    assert expected == result


def test_ignore_enrich_errors():
    path = os.path.join(DATA_DIR, "test_error.log")

    with open(path) as file:
        result = list(
            enrich_errors(
                parse_stream(file, include_raw=True),
                regexes_to_ignore=[".*not installed.*", ".*Failed.*"],
            )
        )
    ignored_error_tags = 0
    for res in result:
        if res.get("error_ignored"):
            ignored_error_tags += 1
    assert ignored_error_tags == 3
