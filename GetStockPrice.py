#!/usr/bin/env python
# coding: utf-8

import os
import random
import re
import time

from requests_html import HTMLSession


def waitedget(session, url, min_wait=3, max_wait=5):
    print(url)
    min_wait = max(min_wait, 3)
    max_wait = max(max_wait, 5)
    time.sleep(max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)), min_wait))
    res = session.get(url)
    res.raise_for_status()
    return res


def waitedpost(session, url, data, min_wait=3, max_wait=5):
    print(url)
    min_wait = max(min_wait, 3)
    max_wait = max(max_wait, 5)
    time.sleep(max(random.normalvariate((min_wait + max_wait) / 2, abs(min_wait - max_wait)), min_wait))
    res = session.post(url, data)
    res.raise_for_status()
    return res


def download_csv(stock_link, basepath):
    year_links = [link for link in waitedget(session, stock_link).html.absolute_links if
                  re.search("/stock/[01-9]+/[01-9]+", link)]
    for year_link in year_links:
        csv_button = waitedget(session, year_link).html.find("form", first=True)
        csv_url = csv_button.attrs['action']
        csv_param = {'_method': csv_button.attrs['method']}
        for input_param in csv_button.find('input'):
            if input_param.attrs['name'] == 'code':
                csv_param["code"] = input_param.attrs['value']
            if input_param.attrs['name'] == 'year':
                csv_param["year"] = input_param.attrs['value']
        res = waitedpost(session, csv_url, data=csv_param)
        res.raise_for_status()  # エラーならここで例外を発生させる
        res = waitedpost(session, url + res.html.find("form", first=True).attrs['action'], data=csv_param)
        res.raise_for_status()  # エラーならここで例外を発生させる
        content_disposition = res.headers['Content-Disposition']
        attribute = 'filename='
        filename = (basepath + content_disposition[content_disposition.find(attribute) + len(attribute):])
        filename = filename.replace('"', "")
        with open(filename, 'wb') as saveFile:
            saveFile.write(res.content)
        print(os.path.abspath(filename))


url = 'https://kabuoji3.com/stock/'
filePath = './datafiles/'
stock_links = []

# Start session

session = HTMLSession()
res = waitedget(session, url)
# get stock page links

for page_link in [link for link in res.html.absolute_links if re.search('page=', link)]:
    res = waitedget(session, page_link)
    for stock_link in [link for link in res.html.absolute_links if re.search('/stock/[01-9]+', link)]:
        print(stock_link)
        download_csv(stock_link, filePath)
