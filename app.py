import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == '__main__':
    log.info('Application is starting...')
    from control import control, pageRanker
    control.start()
    # pageRanker.run()
