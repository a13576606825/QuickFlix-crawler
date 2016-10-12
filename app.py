import logging

__author__ = 'xinzzhou'


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == '__main__':
    log.info('Application is starting...')
    from control import control
    control.start()
