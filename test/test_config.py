# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)

import os
import unittest

from loog.config import LoogConfig

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = LoogConfig(os.path.join(DATA_DIR, "test1.cfg"))

    def test1(self):
        assert self.config.get("test", "absent") is None
        assert self.config.get("test", "absent", "default") == "default"
        assert self.config.get("test", "bool") == "yes"
        assert self.config.get("test", "multi") == "\nABC\nDEF"
        assert self.config.get("test", "multi", flatten=True) == "ABCDEF"
        assert self.config.getboolean("test", "bool") is True
        assert self.config.getboolean("test", "absent") is None
        assert self.config.getboolean("test", "absent", False) is False
        assert self.config.getlist("test", "multi") == ["ABC", "DEF"]
        assert self.config.getlist("test", "absent") == []
        assert self.config.getlist("test", "absent", ["A", "B"]) == ["A", "B"]
        assert self.config.get("absent", "absent") is None
        assert self.config.getboolean("absent", "absent") is None
        assert self.config.getlist("absent", "absent") == []

    def test2(self):
        assert self.config.getlist("check", "ignore") == [".*ERROR.*", ".*CRITICAL.*"]
        assert self.config.getboolean("check", "err-if-err") is True
        assert self.config.getboolean("check", "human-readable") is False
