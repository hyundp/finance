import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ana2
import analyzer
from mpl_finance import candlestick_ohlc
from slacker import Slacker
from datetime import datetime
from datetime import timedelta
import pandas as pd

slack = Slacker('slack code')
def dbgout(message):
    """출력"""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    py = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
    slack.chat.post_message('매매종목', py)

a = ana2.MarketDB()
b = analyzer.MarketDB()

df = a.get_daily_price2()
dk = df.code.drop_duplicates()
# 지금 0,125,250 이렇게 순서로 되어있음 이걸 0,1,2이렇게 바꿔야함.
dk = dk.reset_index(drop=True)
# 이제 남은건 코드만 들어가면 그 코드의 날짜별 가격들이 뜨는 코드를 짜면됨.
for d in dk:
    dj = b.get_daily_price(d)
    dj['MA20'] = dj['close'].rolling(window=20).mean() 
    dj['stddev'] = dj['close'].rolling(window=20).std() 
    dj['upper'] = dj['MA20'] + (dj['stddev'] * 2)
    dj['lower'] = dj['MA20'] - (dj['stddev'] * 2)
    dj['PB'] = (dj['close'] - dj['lower']) / (dj['upper'] - dj['lower'])

    dj['II'] = (2*dj['close']-dj['high']-dj['low'])/(dj['high']-dj['low'])*dj['volume']
    dj['IIP21'] = dj['II'].rolling(window=21).sum()/dj['volume'].rolling(window=21).sum()*100
    dj = dj.dropna()
 
    for i in range(0, len(dj.close)):
        end_date = datetime.today().strftime('%Y-%m-%d')
        six_month_ago = datetime.today() - timedelta(days=180)
        start_date = six_month_ago.strftime('%Y-%m-%d')
        codes_keys = list(b.codes.keys())
        codes_values = list(b.codes.values())
        idx = codes_keys.index(dj.code[0])
        x = codes_values[idx]
        if datetime.today().weekday() == 5:
            end_date = datetime.today() - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')
        if datetime.today().weekday() == 6:
            end_date = datetime.today() - timedelta(days=2)
            end_date = end_date.strftime('%Y-%m-%d')
        if dj.PB.values[i] < 0.05 and dj.IIP21.values[i] > 0 and dj.volume[i] > 70000 and dj.date[i].strftime('%Y-%m-%d') == end_date:
            dbgout("`볼랜더매수" + ' : ' + x + "`")          
        if dj.PB.values[i] > 0.95 and dj.IIP21.values[i] < 0 and dj.volume[i] > 70000 and dj.date[i].strftime('%Y-%m-%d') == end_date:
            dbgout("`볼랜더매도" + ' : ' + x + "`")


for f in dk:
    dj = b.get_daily_price(f)
    ema60 = dj.close.ewm(span=60).mean()
    ema130 = dj.close.ewm(span=130).mean()
    macd = ema60 - ema130
    signal = macd.ewm(span=45).mean()
    macdhist = macd - signal
    dj = dj.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()
    dj['number'] = dj.index.map(mdates.date2num)
    ohlc = dj[['number','open','high','low','close']]
    ndays_high = dj.high.rolling(window=14, min_periods=1).max()
    ndays_low = dj.low.rolling(window=14, min_periods=1).min()
    fast_k = (dj.close - ndays_low) / (ndays_high - ndays_low) * 100
    slow_d = fast_k.rolling(window=3).mean()
    dj = dj.assign(fast_k=fast_k, slow_d=slow_d).dropna()

    for i in range(1, len(dj.close)):
        end_date = datetime.today().strftime('%Y-%m-%d')
        six_month_ago = datetime.today() - timedelta(days=180)
        start_date = six_month_ago.strftime('%Y-%m-%d')
        codes_keys = list(b.codes.keys())
        codes_values = list(b.codes.values())
        idx = codes_keys.index(dj.code[0])
        x = codes_values[idx]
        if datetime.today().weekday() == 5:
            end_date = datetime.today() - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')
        if datetime.today().weekday() == 6:
            end_date = datetime.today() - timedelta(days=2)
            end_date = end_date.strftime('%Y-%m-%d')
        
        if dj.ema130.values[i-1] < dj.ema130.values[i] and \
           dj.slow_d.values[i-1] >= 20 and dj.slow_d.values[i] < 20 and dj.volume[i] > 70000 and dj.date[i].strftime('%Y-%m-%d') == end_date:
            dbgout("`삼중창매수" + ' : ' + x + "`") 
        elif dj.ema130.values[i-1] > dj.ema130.values[i] and \
             dj.slow_d.values[i-1] <= 80 and dj.slow_d.values[i] > 80 and dj.volume[i] > 70000 and dj.date[i].strftime('%Y-%m-%d') == end_date:
            dbgout("`삼중창매도" + ' : ' + x + "`")





    
