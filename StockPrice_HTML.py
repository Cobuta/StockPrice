#!/usr/bin/env python
# coding: utf-8

# In[33]:


from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import pandas as pd
from urllib.parse import urljoin
import PriceDataFrame
from HTML_API import waited_get
import pathlib as path

url = 'https://kabuoji3.com/stock/'
filePath = './datafiles/'

stock_list_header = ('code', 'issue', 'market')

stockprice_df = PriceDataFrame.load_price_df(filePath)
# retrieved_df = PriceDataFrame.retrieved_df(stockprice_df)

# Start session

session = HTMLSession()
res = waited_get(session, url)

# stock list
stock_df = pd.DataFrame(columns=stock_list_header)
# In[36]:

# print(stock_df)
for page_link in [link for link in res.html.absolute_links if re.search('page=', link)]:
    res = waited_get(session, page_link)
    df = pd.read_html(res.text)[0][['コード・名称', '市場']]
    df = pd.concat([df['コード・名称'].str.split(' ', 1, expand=True), df['市場']], axis=1)
    df.columns = stock_list_header
    stock_df = stock_df.append(df)
    print(str(len(stock_df)) + ' issue names are captured.\r')

for code in stock_df['code']:
    print(urljoin(url, str(code)))
    res = waited_get(session, urljoin(url, str(code) + '/'))
    year_links = [link for link in res.html.absolute_links if re.search("/stock/[01-9]+/[01-9]+", link)]
    for year_link in year_links:
        print(year_link)
        res = waited_get(session, year_link)
        year=0
        for input_param in res.html.find("form", first=True).find('input'):
            if input_param.attrs['name'] == 'year': year = input_param.attrs['value']
        if PriceDataFrame.is_exist(stockprice_df, code, year):
            print('skipped')
            continue
        else:
            df = pd.read_html(res.text)[0]
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
            df['code'] = code
            df['issue'] = stock_df[(stock_df['code'] == code)]['issue'].values[0]
            df['market'] = stock_df[(stock_df['code'] == code)]['market'].values[0]
            df['date'] = pd.to_datetime(df['date'])
            print(df)
            df.to_csv(path.Path.joinpath(path.Path(filePath), '../tablefiles/', str(code) + '_' + str(year) + '.csv'))
            stockprice_df = stockprice_df.append(df)

# In[39]:


print(stock_df)

# In[23]:


res.text
