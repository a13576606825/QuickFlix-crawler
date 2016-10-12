import os
import yaml

def _load_config(domain):
    return yaml.safe_load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            domain + '.yml')))

def read(domain, name):
    # TODO: Add multi-level support.
    return _load_config(domain)[name]


def save(domain, name, value):
    pass
