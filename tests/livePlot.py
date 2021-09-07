import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import datetime as dt
import pandas_datareader as web
import time
import pandas as pd

def index_to(tik, start=100):
    r = tik['Close']/tik['Close'].shift(1)
    r.iloc[0] = start
    perf = np.cumprod(r)
    return perf

def ma(tik,length):
    return tik.rolling(length).mean()

def trade(tik, line, shortbelow=False, start=100):
    belowmult = 0
    if shortbelow:
        belowmult = -1
    strat_pct_chg = tik.copy()
    strat_pct_chg = strat_pct_chg/strat_pct_chg.shift(1) -1
    #strat_pct_chg = strat_pct_chg * -1
    strat_pct_chg.loc[tik.shift(1) < line.shift(1)] = strat_pct_chg * belowmult
    strat_pct_chg.iloc[0] = 0
    strat_perf = [start]
    for i in range(1,len(tik)-1):
        strat_perf.append(strat_perf[i-1] * (1+strat_pct_chg[i+1]))
    return strat_perf

def sharpe(perf):
    rets = perf / perf.shift(1) -1
    sharpe = rets.mean() / rets.std()
    return sharpe * (252**.5)

def my_function(i):
    window_width = 100
    """
    Requires dataframe with single column as tiker
    """
    try:
        if(i > window_width):
            plt.xlim(tik.index[i-window_width], tik.index[i])
        else:
            plt.xlim(tik.index[0], tik.index[i])
        
        plt.plot([tik.index[i],tik.index[i+1]],[tik[i],tik[i+1]],'b-')
        plt.plot([tik.index[i],tik.index[i+1]],[tikma[i],tikma[i+1]],'g-')
        plt.plot([tik.index[i],tik.index[i+1]],[perf[i],perf[i+1]],'r-')
    except:
        time.sleep(.5)
        plt.xlim(tik.index[0],tik.index[-1])
        plt.text(tik.index[-100],min(min(tik),min(perf)),'Sharpe:', verticalalignment = 'top')

start = dt.datetime(2020,1,1)
end = dt.datetime(2021,4,20)

tik = input('Enter a tiker: ')
malength = int(input('Enter MA length: '))
belowShort = 0

tik = web.DataReader(tik, 'yahoo', start, end)
fig = plt.figure()

tik = index_to(tik)

tikma = ma(tik,malength)

perf = trade(tik,tikma,shortbelow=belowShort)

animation = FuncAnimation(fig, my_function, interval=10)

plt.show()