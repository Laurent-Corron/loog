

# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import pytest
from loog.parser import parseFile
from loog.parser import _parse

from click.testing import CliRunner

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
class TestParser:
    def test_parse(self):
        path=os.path.join(DATA_DIR, "test1.log")
        with open(path) as file:
            result = next(_parse(file))
            expected = {'levelname': 'INFO', 'db': '?', 'logger': 'odoo', 'message': 'Odoo version 10.0'}
            assert  expected == result

    def test_empty(self):
        path=os.path.join(DATA_DIR, "empty.log")
        with open(path) as file:
            parser = _parse(file)
            with pytest.raises(StopIteration):
                next(parser)
    
    def test_emtpy_parseFile(self):
        path=os.path.join(DATA_DIR, "empty.log")
        with open(path) as file:
            parser = parseFile(file)
            assert parser == []