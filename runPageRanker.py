import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == '__main__':
    log.info('Page Ranker is running')
    from control import pageRanker
    pageRanker.run()
