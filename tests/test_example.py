import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt
import pandas_datareader as pdr

fig = plt.figure()
ax = fig.add_subplot()

MAX = 20

spy = pdr.DataReader('SPY', 'yahoo', dt.datetime(2020,1,1), dt.datetime(2021,1,1))
print(spy.head())

def animate(i):
    x = spy.index[max(0, i-MAX):i]
    y = spy['Close'][max(0, i-MAX):i]
    ax.clear()
    ax.plot(x, y)

    #plt.plot(spy.index[i], spy['Close'][i], 'ro')
    print(i)

anim = FuncAnimation(fig, animate, interval=100)

plt.show()