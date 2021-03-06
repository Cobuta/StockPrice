import random
import time
from http.client import RemoteDisconnected

from requests_html import HTMLSession
from requests import RequestException
from requests import Response


def wait_time(min_wait=3, max_wait=5, *, logger):
    min_wait = max(min_wait, 3)
    max_wait = max(max_wait, 5)
    wait = max(random.normalvariate((min_wait + max_wait) / 2, abs((min_wait - max_wait)/4)), min_wait)
    logger.debug('wait time ' + str(wait))
    return wait


def waited_get(session: HTMLSession, url, min_wait=1, max_wait=1, *, logger):
    #    print(url)
    res = Response()
    logger.debug('get_requested ' + url)
    time.sleep(wait_time(min_wait, max_wait, logger=logger))
    try:
        res = session.get(url)
        res.raise_for_status()
        logger.debug('get_processed ' + url)
    except (RemoteDisconnected, RequestException,OSError) as e:
        logger.critical(url + " error " + str(e))
    finally:
        return res


def waited_post(session: HTMLSession, url, data, min_wait=1, max_wait=1, *, logger):
    #    print(url)
    res = Response()
    logger.debug('post_requested ' + url)
    time.sleep(wait_time(min_wait, max_wait, logger=logger))
    try:
        res = session.post(url, data)
        res.raise_for_status()
        logger.debug('post_processed ' + url)
    except (RemoteDisconnected, RequestException, OSError) as e:
        logger.critical(url + " error " + str(e))
    finally:
        return res
