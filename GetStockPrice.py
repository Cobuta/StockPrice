#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re, random,time,os

def waitedget(session,url,min_wait=3, max_wait=5):
    print(url)
    min_wait=max(min_wait,3)
    max_wait=max(max_wait,5)
    time.sleep(max(random.normalvariate((min_wait+max_wait)/2,abs(min_wait-max_wait)),min_wait))
    res=session.get(url)
    res.raise_for_status()
    return(res)

def waitedpost(session,url,data,min_wait=3, max_wait=5):
    print(url)
    min_wait=max(min_wait,3)
    max_wait=max(max_wait,5)
    time.sleep(max(random.normalvariate((min_wait+max_wait)/2,abs(min_wait-max_wait)),min_wait))
    res=session.post(url,data)
    res.raise_for_status()
    return(res)

def download_csv(stock_link,basepath):
    year_links=[link for link in waitedget(session,stock_link).html.absolute_links if re.search("/stock/[01-9]+/[01-9]+",link)]
    for year_link in year_links:
        csv_button=waitedget(session,year_link).html.find("form",first=True)
        csv_url=csv_button.attrs['action']
        csv_param={'_method':csv_button.attrs['method']}
        for input in csv_button.find('input'):
            if input.attrs['name']=='code':
                csv_param["code"]=input.attrs['value']
            if input.attrs['name']=='year':
                csv_param["year"]=input.attrs['value']
        res = waitedpost(session,csv_url, data=csv_param)
        res.raise_for_status()  # エラーならここで例外を発生させる
        csv_url=url+res.html.find("form",first=True).attrs['action']
        res = waitedpost(session,url+res.html.find("form",first=True).attrs['action'], data=csv_param)
        res.raise_for_status()  # エラーならここで例外を発生させる
        contentType = res.headers['Content-Type']
        contentDisposition = res.headers['Content-Disposition']
        ATTRIBUTE = 'filename='
        fileName = (basepath+contentDisposition[contentDisposition.find(ATTRIBUTE) + len(ATTRIBUTE):]).replace('"',"")
        with open(fileName, 'wb') as saveFile:
                saveFile.write(res.content)
        print(os.path.abspath(fileName))


url = 'https://kabuoji3.com/stock/'
filePath='./datafiles/'
stock_links=[]

# Start session

session = HTMLSession()
res = waitedget(session,url)
res.text
# get stock page links
page_links=[link for link in res.html.absolute_links if re.search('page=',link)]

for plink in page_links:
    res=waitedget(session,plink)
    for stock_link in [link for link in res.html.absolute_links if re.search('/stock/[01-9]+',link)]:
        print(stock_link)
        download_csv(stock_link,filePath)
