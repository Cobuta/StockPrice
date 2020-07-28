import pathlib as path
import re
import Declaration

import pandas as pd
from pandas import DataFrame


def load_price_df(base_path):
    stockprice_df = DataFrame()
    base_folder = path.Path(base_path).expanduser().resolve()
    for f in sorted(base_folder.resolve(strict=True).glob('*.csv')):
        with f.open(encoding='shift_jis') as fobj:
            header_values = re.split('[ ,]', re.sub("[,\n]+$", "", fobj.readline()), 2)
            header = dict(zip(Declaration.header_keys, header_values))
        df1 = pd.read_csv(f, encoding='shift_jis', skiprows=2, index_col=False, names=Declaration.field_names)
        for k in header.keys():
            df1[k] = header[k]
        stockprice_df = pd.concat([stockprice_df, df1])
        print('loaded ' + str(len(stockprice_df)) + ' records\r',end='')
    stockprice_df['date'] = pd.to_datetime(stockprice_df['date'])
    return stockprice_df


def retrieved_df(base_path):
    base_folder = path.Path(base_path).expanduser().resolve()
    df = pd.DataFrame(columns=['code', 'year'])
    i=0
    for f in sorted(base_folder.resolve(strict=True).glob('*.csv')):
        fname_elements = re.split('[_\.]', f.name)
        df = df.append(pd.Series([fname_elements[0], fname_elements[1]], index=['code', 'year']), ignore_index=True)
        i+=1
        print('['+str(i)+']: '+f.name + ' processed.\r',end='')
    df.drop_duplicates(inplace=True)
    df.to_csv(path.Path.joinpath(base_folder, '.retrieved.csv'))
    return df


def is_exist(df, code: str, year: int):
    df = pd.concat([df['date'].dt.year, df['code']], axis=1).drop_duplicates().rename(columns={'date': 'year'})
    df = ((df['year'] == str(year)) & (df['code'] == str(code)))
    # print(df)
    return df.sum() > 0
