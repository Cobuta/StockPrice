import random
import time
from requests_html import HTMLSession


def wait_time(min_wait=1, max_wait=2,*,logger):
    min_wait = max(min_wait, 1)
    max_wait = max(max_wait, 2)
    wait=max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)), 1)
    logger.debug('wait time '+str(wait))
    return wait


def waited_get(session, url, min_wait=3, max_wait=5,*,logger):
    #    print(url)
    logger.debug('get requested '+url)
    time.sleep(wait_time(min_wait, max_wait,logger=logger))
    try:
        res = session.get(url)
        res.raise_for_status()
    except:
        res=None
    logger.debug('get processed '+url)
    return res


def waited_post(session, url, data, min_wait=3, max_wait=5,*,logger):
    #    print(url)
    logger.debug('post requested '+url)
    time.sleep(wait_time(min_wait, max_wait,logger=logger))
    try:
        res = session.post(url, data)
        res.raise_for_status()
    except:
        res = None
    logger.debug('post processed '+url)
    return res
