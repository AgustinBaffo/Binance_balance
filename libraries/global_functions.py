import numpy as np
import time
from datetime import date, timedelta

import yfinance as yf


def next_day(str_date):
    '''
    Return next day
    Input/output format: YYYY-MM-DD
    '''
    t=time.strptime(str_date.replace("-",''),'%Y%m%d')
    return date(t.tm_year,t.tm_mon,t.tm_mday)+timedelta(1)


def get_token_price_by_date(token_name, operation_time):
    '''
    Returns the price of the specified token at the desired time
    token_name (ex.): "BTC" 
    operation_time (ex.): "2021-05-12 14:58:21" -> string
    '''
    operation_day, operation_hr = operation_time.split(" ")
    operation_hr = int(operation_hr.split(":")[0]) # UTC (include +3 ARG)
    if operation_hr>20: # yfinance doesn't return 23:00:00 period
        operation_hr -=1

    try:
        # df = yf.download(tickers='BTC-USD', period = '2h', interval = '15m')
        df = yf.download(tickers=token_name+"-USD", start=operation_day, end=next_day(operation_day), interval = '1h');
        df.index = df.index.tz_localize(None)
    except:
        print("[yfinance] No data found for "+str(token_name)+"-USD")
        return -1

    token_price_usd = np.array(df.iloc[operation_hr][["Open","Close"]]).mean() # Mean between open a close at that hour

    return float(token_price_usd)



