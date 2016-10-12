import logging

log = logging.getLogger()


def print_as_json(thing):
    import json
    log.debug(json.dumps(thing))
