# aiohttpdemo_polls/settings.py
import pathlib
import yaml


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'default.yaml'
print('config: {}'.format(config_path))

config = get_config(config_path)
