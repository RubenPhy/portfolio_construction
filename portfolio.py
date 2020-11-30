import eikon as ek
import pandas as pd
import numpy as np
import datetime
import os


# Read and save the data
def read_data(ticker, start_date, end_date):
    file_name = os.path.join('Data', ticker + '.xlsx')
    try:
        df = pd.read_excel(file_name, index_col='Date')
        df.rename(columns={'CLOSE': ticker}, inplace=True)
        return df
    except FileNotFoundError:
        print('File not found!!', file_name)
        df = ek.get_timeseries(ticker, fields=["Close"],
                               start_date=start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                               end_date=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                               interval='daily')
        df.to_excel(file_name)
        return df
    except Exception:
        print('Another Error!!')
        return None


# Merge and clean historical data
def merge_df(dfs):
    df_merge = pd.concat(dfs, axis=1)
    df_merge.dropna(inplace=True)
    return df_merge


# Annualized return
def annual_returns(df):
    columns = []
    data = []
    for year in sorted(set(df.index.year)):
        df_for_a_year = df[df.index.year == year]
        date_max = df_for_a_year.index.max()
        date_min = df_for_a_year.index.min()
        data.append((df.loc[date_max] / df.loc[date_min] - 1).to_list())
        columns.append(year)

    index = df.columns.values
    data = map(list, zip(*data))
    return pd.DataFrame(data=data, columns=columns, index=index)


# Volatility
def annual_volatility(df):
    df_pct_change = df.pct_change().dropna()
    columns = []
    data = []
    for year in sorted(set(df_pct_change.index.year)):
        df_for_a_year = df_pct_change[df_pct_change.index.year == year]
        annual_volatility_year = (df_for_a_year.std()*np.sqrt(len(df_for_a_year))).to_list()
        data.append(annual_volatility_year)
        columns.append(year)

    index = df_pct_change.columns.values
    data = map(list, zip(*data))
    return pd.DataFrame(data=data, columns=columns, index=index)


# Max dorwdawn


# Correlation


# VaR for a given iterval


if __name__ == '__main__':
    tickers = {'ETF WATER': {'Name': 'ISHSII-GLOBAL WATER UCITS ETF',
                             'RIC': 'IH2O.L',
                             'ISIN': 'IQQQ',
                             'Definition': 'Water traker'},
               'ETF IG 7-10': {'Name': 'AMUNDI ETF IG 7-10',
                               'ISIN': 'FR0010754184',
                               'RIC': 'C73.PA'},
               'ETF S&P': {'Name': 'ISHARES CORE S&P 500 UCITS ETF USD ACC REG. SHARES USD (ACC) O.N.',
                           'RIC': 'CSPX.L',
                           'ISIN': 'IE00B5BMR087'}, }

    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2020, 11, 1)

    df1 = read_data(tickers['ETF WATER']['RIC'], start_date, end_date)
    df2 = read_data(tickers['ETF IG 7-10']['RIC'], start_date, end_date)
    df3 = read_data(tickers['ETF S&P']['RIC'], start_date, end_date)
    df = merge_df([df1, df2, df3])