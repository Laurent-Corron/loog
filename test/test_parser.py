# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

import os

from loog import parse_stream

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestParser:
    def test_parse(self):
        path = os.path.join(DATA_DIR, "test1.log")
        with open(path) as file:
            result = next(parse_stream(file))
            expected = {
                "asctime": "2017-05-21 14:01:49,686",
                "pid": "8038",
                "levelname": "INFO",
                "dbname": "?",
                "logger": "odoo",
                "message": "Odoo version 10.0",
                "raw": "2017-05-21 14:01:49,686 8038 INFO ? odoo: Odoo version 10.0\n",
            }
            assert expected == result

    def test_empty(self):
        path = os.path.join(DATA_DIR, "empty.log")
        with open(path) as file:
            assert list(parse_stream(file)) == []
