import yaml
import os


class YamlReader(object):
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("YAML FILE IS NOT EXISTS")
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yamlf) as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data


if __name__ == '__main__':
    '''Test read yaml file'''
    BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    config_path = os.path.join(BASE_PATH, 'config', 'config.yml')
    test = YamlReader(config_path).data
    for info in test:
        for config in info.values():
            print(config)