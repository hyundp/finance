import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ana2
import analyzer
from mpl_finance import candlestick_ohlc
from slacker import Slacker
from datetime import datetime
from datetime import timedelta
import pandas as pd

a = ana2.MarketDB()
b = analyzer.MarketDB()

df = a.get_daily_price2('2020-11-20', '2020-11-20')
df2 = a.get_daily_price2('2020-11-19', '2020-11-19')

def find (x):
    k = (df.close-df2.close)/df2.close*100
    j = (df.high-df2.close)/df2.close*100
    k = k[j >x]
    m = k-x

    return m
    
    
