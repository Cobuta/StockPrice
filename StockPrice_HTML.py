#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pathlib as path
import re
from urllib.parse import urljoin

import pandas as pd
from requests_html import HTMLSession

import Declaration
import PriceDataFrame
from Declaration import filePath
from HTML_API import waited_get

# stockprice_df = PriceDataFrame.load_price_df(filePath)
retrieved_df = PriceDataFrame.retrieved_df(filePath)

# Start session

session = HTMLSession()
res = waited_get(session, Declaration.url)

# stock list
stock_df = pd.DataFrame(columns=Declaration.stock_list_header)
# In[36]:

# print(stock_df)
for page_link in [link for link in res.html.absolute_links if re.search('page=', link)]:
    res = waited_get(session, page_link)
    df = pd.read_html(res.text)[0][['コード・名称', '市場']]
    df = pd.concat([df['コード・名称'].str.split(' ', 1, expand=True), df['市場']], axis=1)
    df.columns = Declaration.stock_list_header
    stock_df = stock_df.append(df)
    print(str(len(stock_df)) + ' issue names are captured.\r')

for code in stock_df['code']:
    print(urljoin(Declaration.url, str(code)))
    res = waited_get(session, urljoin(Declaration.url, str(code) + '/'))
    year_links = [link for link in res.html.absolute_links if re.search("/stock/[01-9]+/[01-9]+", link)]
    for year_link in year_links:
        print(year_link)
        year = year_link.split('/')[-2]
        code = year_link.split('/')[-3]
        if ((retrieved_df['year'] == year) & (retrieved_df['code'] == code)).sum() > 0:
            print('skipped')
            continue
        else:
            res = waited_get(session, year_link)
            if res==None: continue
            df = pd.read_html(res.text)[0]
            df.columns = Declaration.field_names
            df['code'] = code
            df['issue'] = stock_df[(stock_df['code'] == code)]['issue'].values[0]
            df['market'] = stock_df[(stock_df['code'] == code)]['market'].values[0]
            df['date'] = pd.to_datetime(df['date'])
            print(df)
            df.to_csv(path.Path(filePath).expanduser().resolve().joinpath(str(code) + '_' + str(year) + '.csv'))
            # stockprice_df = stockprice_df.append(df)

# In[39]:


print(stock_df)

# In[23]:


