# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)

import os
from configparser import NoOptionError, NoSectionError, RawConfigParser

import click

DEFAULT_CONFIG_FILE = "loog.cfg"


def _split_multiline(s):
    return [i.strip() for i in s.splitlines() if i.strip()]


class LoogConfig(object):

    # list of callables returning dictionaries to update default_map
    default_map_readers = []

    def __init__(self, filename):
        self.__cfg = RawConfigParser()
        if not filename and os.path.isfile(DEFAULT_CONFIG_FILE):
            filename = DEFAULT_CONFIG_FILE
        if filename:
            if not os.path.isfile(filename):
                raise click.ClickException(
                    "Configuration file {} not found.".format(filename)
                )
            self.__cfgfile = filename
            self.__cfg.read(filename)

    def get_default_map(self):
        default_map = {}
        for reader in self.default_map_readers:
            default_map.update(reader(self))
        return default_map

    @staticmethod
    def add_default_map_reader(reader):
        LoogConfig.default_map_readers.append(reader)

    def get(self, section, option, default=None, flatten=False):
        try:
            r = self.__cfg.get(section, option)
            if flatten:
                r = "".join(_split_multiline(r))
            return r
        except (NoOptionError, NoSectionError):
            return default

    def getboolean(self, section, option, default=None):
        try:
            return self.__cfg.getboolean(section, option)
        except (NoOptionError, NoSectionError):
            return default

    def getlist(self, section, option, default=None):
        try:
            return _split_multiline(self.__cfg.get(section, option))
        except (NoOptionError, NoSectionError):
            return default or []
