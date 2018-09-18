import os
from utils.file_reader import YamlReader


BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
APK_PATH = os.path.join(BASE_PATH, 'apk')
TOOLS_PATH = os.path.join(BASE_PATH, 'tools')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')


class Config(object):
    def __init__(self, config=CONFIG_FILE):
        self.configs = YamlReader(config).data

    def get(self):
        for info in self.configs:
            for config in info.values():
                yield config


if __name__ == "__main__":
    c = Config()
    for i in c.get():
        print(i)