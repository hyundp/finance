import datetime

import matplotlib.dates as mdates

import ana2
import analyzer
from slacker import Slacker

slack = Slacker('')


def dbgout(message):
    """출력"""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    py = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
    slack.chat.post_message('invester', py)


a = ana2.MarketDB()
b = analyzer.MarketDB()

df = a.get_daily_price2()
dk = df.code.drop_duplicates()
dk = dk.reset_index(drop=True)

for f in dk:
    dj = b.get_daily_price(f)
    ema60 = dj.close.ewm(span=60).mean()
    ema130 = dj.close.ewm(span=130).mean()
    macd = ema60 - ema130
    signal = macd.ewm(span=45).mean()
    macdhist = macd - signal
    dj = dj.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()

    dj['number'] = dj.index.map(mdates.date2num)
    ohlc = dj[['number', 'open', 'high', 'low', 'close']]

    ndays_high = dj.high.rolling(window=14, min_periods=1).max()
    ndays_low = dj.low.rolling(window=14, min_periods=1).min()

    fast_k = (dj.close - ndays_low) / (ndays_high - ndays_low) * 100
    slow_d = fast_k.rolling(window=3).mean()
    dj = dj.assign(fast_k=fast_k, slow_d=slow_d).dropna()

    for i in range(1, len(dj.close)):
        if dj.ema130.values[i - 1] < dj.ema130.values[i] and \
                dj.slow_d.values[i - 1] >= 20 and dj.slow_d.values[i] < 20:
            dbgout("`매수" + ' : ' + x + "`")
        elif dj.ema130.values[i - 1] > dj.ema130.values[i] and \
                dj.slow_d.values[i - 1] <= 80 and dj.slow_d.values[i] > 80:
            dbgout("`매도" + ' : ' + x + "`")
