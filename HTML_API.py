import pathlib as path
import random
import re
import time

from requests_html import HTMLSession


def wait_time(min_wait=1, max_wait=2):
    min_wait = max(min_wait, 1)
    max_wait = max(max_wait, 2)
    return max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)) / 4, min_wait)


def waited_get(session, url, min_wait=3, max_wait=5):
    #    print(url)
    time.sleep(wait_time(min_wait, max_wait))
    res = session.get(url)
    res.raise_for_status()
    return res


def waited_post(session, url, data, min_wait=3, max_wait=5):
    #    print(url)
    time.sleep(wait_time(min_wait, max_wait))
    res = session.post(url, data)
    res.raise_for_status()
    return res
