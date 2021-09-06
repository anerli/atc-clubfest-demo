import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf
import pandas as pd
import random

# Create tk window root
root = tk.Tk()

# Create fig
fig = plt.figure()

# Pack fig into root
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky='snew')#.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create new subplot (important to do this after packing)
ax = fig.add_subplot()

# Setup data
window = 100
sma_window = 20

sp500 = pd.read_csv('S&P500-Symbols.csv')['Symbol'].to_list()

def reset_data():
    global close
    global sma
    global y_height
    global ticker
    
    ticker = random.choice(sp500)
    root.title(f'Automated Trader (Trading {ticker})')

    data = yf.download(ticker,'2000-01-01','2021-01-01')
    close = data['Adj Close']
    sma = close.rolling(window=50).mean()
    y_height = max(close)

reset_data()

# Setup algo
initial_cash = 10000
cash = initial_cash
shares = 0

cash_label = tk.Label(master=root, font=('Consolas', 48), borderwidth=1, relief="solid")
cash_label.grid(row=0, column=0, sticky='snew')
shares_label = tk.Label(master=root, font=('Consolas', 48), borderwidth=1, relief="solid")
shares_label.grid(row=0, column=1, sticky='snew')

last_action_label = tk.Label(master=root, font=('Consolas', 24), borderwidth=1, relief="solid", text='test123')
last_action_label.grid(row=1, column=0, columnspan=2, sticky='snew')

total_value_label = tk.Label(master=root, font=('Consolas', 32), borderwidth=1, relief="solid")
total_value_label.grid(row=3, column=0, sticky='snew') # 'snew' == 'ew' in this context
profit_label = tk.Label(master=root, font=('Consolas', 32), borderwidth=1, relief="solid")
profit_label.grid(row=3, column=1, sticky='snew')

# Uniform groups: ensure all columns in same group have uniform spacing
root.grid_columnconfigure(0, weight=1, uniform='group1')
root.grid_columnconfigure(1, weight=1, uniform='group1')
root.grid_rowconfigure(2, weight=1)

def buy_max(price):
    global cash
    global shares
    max_purchasable = cash // price
    cash -= max_purchasable*price
    shares += int(max_purchasable)
    if max_purchasable > 0:
        last_action_label['text'] = f'Last Action: Bought {int(max_purchasable)} shares of {ticker} at ${price:.2f} for a total of ${max_purchasable*shares:.2f}'

def sell_max(price):
    global cash
    global shares
    cash += price*shares
    if shares > 0:
        last_action_label['text'] = f'Last Action: Sold {shares} shares of {ticker} at ${price:.2f} for a total of ${price*shares:.2f}'
    shares = 0

# Animate function
def animate(t):
    #print(t)
    global close
    global sma
    global y_height
    global sma_window

    #global anim

    current_time = t + window
    # Drawing logic
    ax.clear()
    #ax.set_ylim(0, y_height+10)
    ax.set_ylim(0, max(close[t:current_time])+10)
    ax.plot(close[t:current_time])
    ax.plot(sma[t:current_time])
    ax.legend([f'{ticker} Close Price', f'{sma_window}-Day Moving Average'])

    # Algorithm logic
    price = close[current_time]
    if sma[current_time] >= price:
        buy_max(price)
    else:
        sell_max(price)

    # Update UI
    cash_label['text'] = f'Cash: ${cash:.2f}'
    shares_label['text'] = f'{shares} Shares {ticker}'
    total_value = cash+shares*price
    total_value_label['text'] = f'Total Liquid Value: ${total_value:.2f}'
    profit = total_value-initial_cash
    if profit == 0:
        profit_label['fg'] = 'black'
    elif profit > 0:
        profit_label['fg'] = 'green'
    else:
        profit_label['fg'] = 'red'
    profit_label['text'] = f'Total Profit: {"-" if profit < 0 else ""}${abs(profit):.2f} ({"-" if profit < 0 else "+"}{abs(profit)/initial_cash*100:.2f}%)'
    #print(f'Cash: {cash:.2f} | Shares: {shares}')

    if t == len(close)-window-1:
        # We are on the last frame
        ax.clear()
        reset_data()

# Create animination object
anim = FuncAnimation(fig, animate, interval=50, frames=range(len(close)-window), repeat=True)

# Run tkinter loop
tk.mainloop()