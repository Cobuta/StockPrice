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

# print(stock_df)
for page_link in ([link for link in res.html.absolute_links if re.search('page=', link)]):
    logger.debug('started ' + page_link)
    stock_df = pd.DataFrame(columns=Declaration.stock_list_header)
    res = waited_get(session, page_link, logger=logger)
    try:
        df = pd.read_html(res.text)[0][['コード・名称', '市場']]
        df = pd.concat([df['コード・名称'].str.split(' ', 1, expand=True), df['市場']], axis=1)
        df.columns = Declaration.stock_list_header
        stock_df = stock_df.append(df)
        logger.debug('processed ' + page_link)

        for code in stock_df['code']:
            base_folder = path.Path(filePath).expanduser().resolve()
            # print(urljoin(Declaration.url, str(code)))
            res = waited_get(session, urljoin(Declaration.url, str(code) + '/'), logger=logger)
            year_links = sorted([link for link in res.html.absolute_links if re.search("/stock/[01-9]+/[01-9]+", link)])
            for year_link in year_links:
                # print(year_link)
                year = year_link.split('/')[-2]
                code = year_link.split('/')[-3]
                if base_folder.joinpath(str(code) + '_' + str(year) + '.csv').is_file():
                    logger.info('skipped ' + year_link)
                    # print('skipped')
                else:
                    logger.debug('started ' + year_link)
                    res = waited_get(session, year_link, logger=logger)
                    try:
                        df = pd.read_html(res.text)[0]
                        df.columns = Declaration.field_names
                        df['code'] = code
                        df['issue'] = stock_df[(stock_df['code'] == code)]['issue'].values[0]
                        df['market'] = stock_df[(stock_df['code'] == code)]['market'].values[0]
                        df['date'] = pd.to_datetime(df['date'])
                        fileName = path.Path(filePath).expanduser().resolve()
                        fileName = fileName.joinpath(str(code) + '_' + str(year) + '.csv')
                        df.to_csv(fileName)
                        print('added ' + fileName.name)
                        logger.info('added ' + fileName.name)
                        logger.debug('processed ' + year_link)
                    except ValueError:
                        logger.warning(year_link + ' has_nothing')
                        continue
    except ValueError:
        logger.warning(page_link + ' has_nothing')
        continue

# In[39]:


# In[23]:
