import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

data = yf.download('AAPL','2016-01-01','2019-08-01')

print(type(data))
print(data.head())

fig = plt.figure()
ax = fig.add_subplot()

# Plot the close price of the AAPL
start = 0
end = 100

dat = data['Adj Close']
y_height = max(dat)


print(y_height)
window = 50

def animate(t):
    print(t)
    ax.clear()
    ax.set_ylim(0, y_height+10)
    #ax.plot(dat[t:t+window])
    ax.plot(dat[0:t])

anim = FuncAnimation(fig, animate, interval=10, frames=range(len(dat)-50))
plt.show()


# dat = data['Adj Close']
# while end < len(dat):
#     #data[start:end].plot()
#     #plt.show()
#     time.sleep(1)
#     start += 1
#     end += 1
# data['Adj Close'][:100].plot()
# plt.show()