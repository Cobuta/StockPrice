#!/usr/bin/env python
# coding: utf-8

__doc__ = """{f}

Usage:
    {f} <URL_or_FILE> [-o|--output <Folder>]
    {f} -h | --help

Options:
    -o --output <Folder>    specify output folder
    -h --help               Show this screen and exit.
""".format(f=__file__)

import pathlib as path
import re
from logging import getLogger, basicConfig, INFO
from urllib.parse import urljoin, urlparse

import pandas as pd
from docopt import docopt
from requests_html import HTMLSession

import Declaration
from HTML_API import waited_get

# global variables

# base_folder = path.Path(__file__).parent
session = HTMLSession()


def get_stock_links(url, folder):  # process root url
    res = waited_get(session, url, logger=logger)
    try:
        page_links = [link for link in res.html.absolute_links if re.search('page=', link)]
    except ValueError:
        logger.critical('invalid_url ' + url)
        raise
    for page_link in page_links:
        logger.debug('started ' + page_link)
        stock_df = pd.DataFrame(columns=Declaration.stock_list_header)
        res = waited_get(session, page_link, logger=logger)
        try:
            df = pd.read_html(res.text)[0][['コード・名称', '市場']]
        except (ValueError,AttributeError) as e:
            logger.warning(page_link + str(e))
        else:
            df = pd.concat([df['コード・名称'].str.split(' ', 1, expand=True), df['市場']], axis=1)
            df.columns = Declaration.stock_list_header
            stock_df = stock_df.append(df)
            logger.debug('processed ' + page_link)
            for code in stock_df['code']:
                stock_link = urljoin(Declaration.url, str(code) + '/')
                get_year_links(stock_link, folder)


def get_year_links(stock_link, folder):
    res = waited_get(session, stock_link, logger=logger)
    try:
        year_links = sorted([link for link in res.html.absolute_links if re.search("/stock/[01-9]+/[01-9]+", link)])
    except (ValueError,AttributeError) as e:
        logger.warning(stock_link + str(e))
    else:
        for year_link in year_links:
            get_stockprice(year_link, folder)


def get_stockprice(year_link, folder):
    year = year_link.split('/')[-2]
    code = year_link.split('/')[-3]
    if folder.joinpath(str(code) + '_' + str(year) + '.csv').is_file():
        logger.info('skipped ' + year_link)
        # print('skipped')
    else:
        logger.debug('started ' + year_link)
        res = waited_get(session, year_link, logger=logger)
        try:
            df = pd.read_html(res.text)[0]
        except (ValueError,AttributeError) as e:
            logger.warning(year_link + str(e))
        else:
            df.rename(columns=Declaration.field_map, inplace=True)
            issue_attrs = res.html.find('meta[name="keywords"]')[0].attrs['content'].split(',')
            df['code'] = code
            df['issue'] = issue_attrs[1]
            df['market'] = issue_attrs[2]
            df['date'] = pd.to_datetime(df['date'])
            file_name = folder.joinpath(str(code) + '_' + str(year) + '.csv')
            df.to_csv(file_name)
            print('added ' + file_name.name)
            logger.info('added ' + file_name.name)
            logger.debug('processed ' + year_link)


def parse_url(url, folder):
    if re.match('http[s]',urlparse(url).scheme):
        url_elements = urlparse(url).path.split('/')
        if re.match('[01-9]+', url_elements[-2]):
            if re.match('[01-9]+', url_elements[-3]):
                # url is stock x year
                get_stockprice(url, folder)
            else:
                # url is stock
                get_year_links(url, folder)
        else:
            # url might be a root
            get_stock_links(url, folder)
    else:
        logger.warning(url+' invalid_url')


def main():
    args = docopt(__doc__)
    if len(args['--output']):
        file_path = args['--output'][0]
    else:
        file_path = path.Path(__file__).parent
    base_folder = path.Path(file_path).expanduser().resolve()
    if path.Path(args['<URL_or_FILE>']).is_file():
        urls = [url for url in path.Path(args['<URL_or_FILE>']).read_text().split('\n') if
                len(url)]  # assume input is file
    else:
        urls = [args['<URL_or_FILE>']]  # assume input is url
    for url in urls:
        parse_url(url, base_folder)


if __name__ == '__main__':
    LogFormat = '{asctime} [{levelname}] {module} {message}'
    basicConfig(filename='stockprice.log', format=LogFormat, style='{', level=INFO)
    logger = getLogger(__name__)
    logger.info('StockPrice retrieval started')
    main()
    logger.info('StockPrice retrieval completed')
