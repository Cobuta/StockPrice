import random
import time
from requests_html import HTMLSession
from requests import RequestException


def wait_time(min_wait=1, max_wait=5, *, logger):
    min_wait = max(min_wait, 1)
    max_wait = max(max_wait, 5)
    wait = max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)), 1)
    logger.debug('wait time ' + str(wait))
    return wait


def waited_get(session: HTMLSession, url, min_wait=1, max_wait=1, *, logger):
    #    print(url)
    logger.debug('get_requested ' + url)
    time.sleep(wait_time(min_wait, max_wait, logger=logger))
    try:
        res = session.get(url )
        res.raise_for_status()
        logger.debug('get_processed ' + url)
    except RequestException as e:
        logger.critical(url + " error " + str(e))
    finally:
        return res


def waited_post(session: HTMLSession, url, data, min_wait=1, max_wait=1, *, logger):
    #    print(url)
    logger.debug('post_requested ' + url)
    time.sleep(wait_time(min_wait, max_wait, logger=logger))
    try:
        res = session.post(url, data)
        res.raise_for_status()
        logger.debug('post_processed ' + url)
    except RequestException as e:
        logger.critical(url + " error " + str(e))
    finally:
        return res
