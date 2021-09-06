import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf

# Create tk window root
root = tk.Tk()
root.title('Automated Trader')

# Create fig
fig = plt.figure()

# Pack fig into root
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create new subplot (important to do this after packing)
ax = fig.add_subplot()

# Setup data
data = yf.download('AAPL','2016-01-01','2019-08-01')
close = data['Adj Close']
window = 100
sma_window = 50
sma = close.rolling(window=50).mean()
y_height = max(close)

# Setup algo
initial_cash = 10000
cash = initial_cash
shares = 0

def buy_max(price):
    global cash
    global shares
    max_purchasable = cash // price
    cash -= max_purchasable*price
    shares += max_purchasable
    #print(f'Selling {shares} shares at ${price} for a total of {price*shares}')

def sell_max(price):
    global cash
    global shares
    cash += price*shares
    shares = 0
    #print(f'Selling {shares} shares at ${price} for a total of {price*shares}')

# Animate function
def animate(t):
    current_time = t + window
    # Drawing logic
    ax.clear()
    ax.set_ylim(0, y_height+10)
    ax.plot(close[t:current_time])
    ax.plot(sma[t:current_time])
    #ax.plot(close[0:t])

    # Algorithm logic
    price = close[current_time]
    if sma[current_time] >= price:
        buy_max(price)
    else:
        sell_max(price)

    print(f'Cash: {cash:.2f} | Shares: {shares}')


# Create animination object
anim = FuncAnimation(fig, animate, interval=50, frames=range(len(close)-window))

# Run tkinter loop
tk.mainloop()