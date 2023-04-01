from __future__ import annotations
import configparser as cfg
import os
from configparser import ExtendedInterpolation

OPENAI_API_KEY = "openai_api_key"


class Configuration:

    @classmethod
    def create_dev_config(cls, file_path:str):
        config = Configuration(file_path)
        return config

    def __init__(self, config_file: str, env_name: str = "dev", common_section_name: str = None):
        self.config_file = os.path.abspath(config_file)
        if not os.path.isfile(self.config_file):
            raise Exception(f"No configuration file:{self.config_file}")
        self.env_name = env_name
        self.config_dir, self.file_name = os.path.split(self.config_file)
        if common_section_name is not None:
            self.common_section_name = common_section_name
        else:
            self.common_section_name = self.get_common_section_name()
        self._read_config_file()

    def get_small_storage_dir(self):
        storage_dir = self['app_small_storage_dir']
        if storage_dir is None:
            storage_dir = os.path.join(self.config_dir, "small.storage")
        if not os.path.isdir(storage_dir):
            os.makedirs(storage_dir)
        return storage_dir

    def _read_config_file(self):
        self.config_all = cfg.ConfigParser(interpolation=ExtendedInterpolation())
        self.config_all.read(self.config_file)
        self.env_config = self.config_all[self.env_name]
        try:
            common_section_name = self.common_section_name
            self.common_config = self.config_all[common_section_name]
        except KeyError as ke:
            print("Could not locate common section in {}".format(self.config_file))
            self.common_config = {}

    @staticmethod
    def get_common_section_name():
        return "common"

    def get_section(self, section_name):
        return self.config_all[section_name]

    def get_section_names(self):
        self.config_all.sections()

    def __getitem__(self, item):
        if item in self.env_config:
            return self.env_config[item]
        if item in self.common_config:
            return self.common_config[item]
        return None

    def get_value(self, key_name, default_value=None):
        v = self.__getitem__(key_name)
        if v is None:
            return default_value

    def __getattr__1(self, item):
        return self.__getitem__(item)


def default_config_file():
    home_dir = os.path.expanduser("~")
    dirname = "ai.config"
    dir_path = os.path.join(home_dir, dirname)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    file_name = "ai.fun.ini"
    return os.path.join(dir_path, file_name)


def create_default_dev_config():
    file_name = default_config_file()
    return Configuration.create_dev_config(file_name)


