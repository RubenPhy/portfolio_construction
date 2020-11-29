import eikon as ek
import pandas as pd
import os


# Read and save the data
def read_data(ticker, start_date, end_date):
    file_name = os.path.join('Data', ticker + '.xlsx')
    try:
        df = pd.read_excel(file_name)
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

# Annualized return

# Volatility


# Max dorwdawn


# VaR for a given iterval
