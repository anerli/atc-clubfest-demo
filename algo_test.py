import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

# Important to use to_frame() else will be a Series
msft = data['MSFT'].to_frame()
msft.rename(columns={'MSFT':'Close'}, inplace=True)

print(msft.head())


sma20 = msft.rolling(window=20).mean()

msft['sma20'] = sma20

print(msft.tail())
print(len(msft))

# Simulate trading algorithm
initial_cash = 10000
cash = initial_cash
stocks_held = 0

def buy_max(price):
    global cash
    global stocks_held
    max_purchasable = cash // price
    cash -= max_purchasable*price
    stocks_held += max_purchasable

def sell_max(price):
    global cash
    global stocks_held
    cash += price*stocks_held
    stocks_held = 0

for t in range(len(msft)):
    price = msft['Close'][t]
    if msft['sma20'][t] >= price:
        buy_max(price)
    else:
        sell_max(price)
    # if t == 0:
    #     print(msft['Close'][t])

final_price = msft['Close'][-1]
sell_max(final_price)
print(f'Final Cash using moving average strategy: ${cash:.2f}')

initial_held = initial_cash // msft['Close'][0]
print(f'Final Cash using buy & hold: ${initial_held*final_price}')





initial_cash = 10000
cash = initial_cash
stocks_held = 0
# plt.plot(msft)
# plt.show()
#print(msft.iloc[::-1]['Close'].to_list())
#msft['Close'] = msft.iloc[::-1]['Close']
#msft = msft.reindex(index=data.index[::-1])
# Use to_list else will auto align with dates
msft['Close'] = msft.iloc[::-1]['Close'].to_list()
#print(msft['Close'])
msft['sma20'] = msft.rolling(window=20).mean()
#plt.plot(msft)
#plt.show()
# What if we had a stock that went down?
for t in range(len(msft)):
    price = msft['Close'][t]
    if msft['sma20'][t] >= price:
        buy_max(price)
    else:
        sell_max(price)
    # if t == 0:
    #     print(msft['Close'][t])


# Here's where the advantage of the moving average strategy reveals itself:
# We profit even though 
final_price = msft['Close'][-1]
#print(final_price)
sell_max(final_price)
print(f'Final Cash using moving average strategy: ${cash:.2f}')

initial_price = msft['Close'][0]
#print(initial_price)
initial_held = initial_cash // initial_price
# print(initial_held)
# print(cash // final_price)
print(f'Final Cash using buy & hold: ${initial_held*final_price}')