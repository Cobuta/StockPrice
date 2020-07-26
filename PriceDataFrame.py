import pathlib as path
import re

import pandas as pd
from pandas import DataFrame


def load_price_df(base_path):
    stockprice_df = DataFrame()
    header_keys = ['code', 'market', 'issue']
    field_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']

    for f in path.Path(base_path).resolve(strict=True).glob('*.csv'):
        with f.open(encoding='shift_jis') as fobj:
            header_values = re.split('[ ,]', re.sub("[,\n]+$", "", fobj.readline()), 2)
            header = dict(zip(header_keys, header_values))
        df1 = pd.read_csv(f, encoding='shift_jis', skiprows=2, index_col=False, names=field_names)
        for k in header.keys():
            df1[k] = header[k]
        stockprice_df = pd.concat([stockprice_df, df1])
    stockprice_df['date'] = pd.to_datetime(stockprice_df['date'])
    return stockprice_df


def retrieved_df(df):
    return pd.concat([df['date'].dt.year, df['code']], axis=1).drop_duplicates().rename(columns={'date': 'year'})


def is_exist(df, code: str, year: int):
    df = pd.concat([df['date'].dt.year, df['code']], axis=1).drop_duplicates().rename(columns={'date': 'year'})
    df = ((df['year'] == int(year)) & (df['code'] == str(code)))
    # print(df)
    return df.sum() > 0
