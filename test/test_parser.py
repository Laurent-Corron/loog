# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import json
import os

from loog import enrich_werkzeug, parse_stream

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_empty():
    path = os.path.join(DATA_DIR, "empty.log")
    with open(path) as file:
        assert list(parse_stream(file)) == []


def test_parsing_file():
    path = os.path.join(DATA_DIR, "test1.log")
    with open(path) as file:
        result = list(parse_stream(file))
        with open(os.path.join(DATA_DIR, "test1_expected.json")) as expected_file:
            expected = json.load(expected_file)
        assert expected == result


def test_parsing_irregular_lines():
    path = os.path.join(DATA_DIR, "test1.log")
    with open(path) as file:
        result = list(parse_stream(file))
        # checks that the first line is added in the first dict
        assert "first line fo the file" in result[0]["raw"]
        assert 1 == len(result[0])
        # checks that the Traceback message was added to the previous line's message
        assert "Traceback" in result[5]["message"]


def test_werkzeug():
    path = os.path.join(DATA_DIR, "testWerkzeug.log")
    with open(path) as file:
        resultParse = list(parse_stream(file))
        # print(resultParse)
        result = list(enrich_werkzeug(resultParse))
        with open(
            os.path.join(DATA_DIR, "testWerkzeug_expected.json")
        ) as expected_file:
            expected = json.load(expected_file)
        assert expected == result[1]

        # result[2] is using oddoo 11's format
        # (without sql_count, sql_time and python_time) so checking its value
        assert "sql_count" not in result[2]["werkzeug"].keys()
        assert "sql_time" not in result[2]["werkzeug"].keys()
        assert "python_time" not in result[2]["werkzeug"].keys()
