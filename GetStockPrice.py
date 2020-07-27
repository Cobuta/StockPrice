#!/usr/bin/env python
# coding: utf-8

import pathlib as path
import random
import re
import time

from requests_html import HTMLSession

import PriceDataFrame
from Declaration import filePath, url
from HTML_API import waited_get, waited_post


def download_csv(stock_link, base_path, stockprice_df):
    year_links = [link for link in waited_get(session, stock_link).html.absolute_links if
                  re.search("/stock/[01-9]+/[01-9]+", link)]
    for year_link in year_links:
        csv_button = waited_get(session, year_link).html.find("form", first=True)
        csv_url = csv_button.attrs['action']
        csv_param = {'_method': csv_button.attrs['method']}
        for input_param in csv_button.find('input'):
            if input_param.attrs['name'] == 'code':
                csv_param["code"] = input_param.attrs['value']
            if input_param.attrs['name'] == 'year':
                csv_param["year"] = input_param.attrs['value']
        if ~PriceDataFrame.is_exist(stockprice_df, csv_param['code'], csv_param['year']):
            res = waited_post(session, csv_url, data=csv_param)
            res.raise_for_status()  # エラーならここで例外を発生させる
            res = waited_post(session, url + res.html.find("form", first=True).attrs['action'], data=csv_param)
            res.raise_for_status()  # エラーならここで例外を発生させる
            content_disposition = res.headers['Content-Disposition']
            attribute = 'filename='
            filename = content_disposition[content_disposition.find(attribute) + len(attribute):].replace('"', "")
            filename = path.Path(base_path).joinpath(filename)
            with open(filename, 'wb') as saveFile:
                saveFile.write(res.content)
            print(path.Path(filename).resolve())
        else:
            print("skipped")




stockprice_df = PriceDataFrame.load_price_df(filePath)
retrieved_df = PriceDataFrame.retrieved_df(stockprice_df)

# Start session

session = HTMLSession()
res = waited_get(session, url)
# get stock page links

for page_link in [link for link in res.html.absolute_links if re.search('page=', link)]:
    res = waited_get(session, page_link)
    for stock_link in [link for link in res.html.absolute_links if re.search('/stock/[01-9]+', link)]:
        print(stock_link)
        download_csv(stock_link, filePath, stockprice_df)
