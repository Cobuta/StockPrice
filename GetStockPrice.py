#!/usr/bin/env python
# coding: utf-8

# In[11]:


from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import random,time

def waitedget(session,url,min_wait=3, max_wait=5):
    print(url)
    min_wait=max(min_wait,3)
    max_wait=max(max_wait,5)
    time.sleep(max(random.normalvariate((min_wait+max_wait)/2,abs(min_wait-max_wait)),min_wait))
    return(session.get(url))

url = 'https://kabuoji3.com/stock'
stock_links=[]

# セッション開始
session = HTMLSession()
res = waitedget(session,url,5,10)


# In[12]:


page_links=[link for link in res.html.absolute_links if re.search('page=',link)]


# In[16]:


for plink in page_links:
    res=waitedget(session,plink)
    stock_links+=[link for link in res.html.absolute_links if re.search('/stock/[01-9]+',link)]


# In[17]:


print(stock_links)

