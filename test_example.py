import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt
import pandas_datareader as pdr

fig = plt.figure()

spy = pdr.DataReader('SPY', 'yahoo', dt.datetime(2020,1,1), dt.datetime(2021,1,1))
print(spy.head())

def animate(i):
    plt.plot(i, spy['Close'][i],'ro')
    print(i)

anim = FuncAnimation(fig, animate, interval=1000)

plt.show()