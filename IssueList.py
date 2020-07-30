#!/usr/bin/env python
# coding: utf-8


import pathlib as path
import re
from logging import getLogger, basicConfig, DEBUG
from urllib.parse import urljoin

import pandas as pd
from requests_html import HTMLSession

import Declaration
from Declaration import filePath
from HTML_API import waited_get

LogFormat = '{asctime} [{levelname}] {module} {message}'
# Formatter(LogFormat, style='{')
basicConfig(format=LogFormat, style='{', level=DEBUG)
logger = getLogger(__name__)

logger.info('StockPrice retrieval started')

# stockprice_df = PriceDataFrame.load_price_df(filePath)
# retrieved_df = PriceDataFrame.retrieved_df(filePath)

# Start session

session = HTMLSession()
res = waited_get(session, Declaration.url, logger=logger)

# stock list
# In[36]:
stock_df = pd.DataFrame(columns=Declaration.stock_list_header)

# print(stock_df)
for page_link in ([link for link in res.html.absolute_links if re.search('page=', link)]):
    logger.debug('started ' + page_link)
    res = waited_get(session, page_link, logger=logger)
    try:
        df = pd.read_html(res.text)[0][['コード・名称', '市場']]
        df = pd.concat([df['コード・名称'].str.split(' ', 1, expand=True), df['市場']], axis=1)
        df.columns = Declaration.stock_list_header
        stock_df = stock_df.append(df)
        logger.debug('processed ' + page_link)
    except ValueError:
        logger.warning(page_link + ' has_nothing')
        continue

stock_df.to_csv('stocklist.csv')