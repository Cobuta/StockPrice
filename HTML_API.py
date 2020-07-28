import random
import time


def wait_time(min_wait=1, max_wait=2):
    min_wait = max(min_wait, 1)
    max_wait = max(max_wait, 2)
    return max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)) / 4, min_wait)


def waited_get(session, url, min_wait=3, max_wait=5):
    #    print(url)
    time.sleep(wait_time(min_wait, max_wait))
    try:
        res = session.get(url)
        res.raise_for_status()
    except:
        res=None
    return res


def waited_post(session, url, data, min_wait=3, max_wait=5):
    #    print(url)
    time.sleep(wait_time(min_wait, max_wait))
    try:
        res = session.post(url, data)
        res.raise_for_status()
    except:
        res = None
    return res
