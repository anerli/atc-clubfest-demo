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
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='snew')#.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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

cash_label = tk.Label(master=root, font=('Consolas', 48), borderwidth=1, relief="solid")
cash_label.grid(row=0, column=0, sticky='snew')
shares_label = tk.Label(master=root, font=('Consolas', 48), borderwidth=1, relief="solid")
shares_label.grid(row=0, column=1, sticky='snew')

total_value_label = tk.Label(master=root, font=('Consolas', 36), borderwidth=1, relief="solid")
total_value_label.grid(row=2, column=0, sticky='snew') # 'snew' == 'ew' in this context
profit_label = tk.Label(master=root, font=('Consolas', 36), borderwidth=1, relief="solid")
profit_label.grid(row=2, column=1, sticky='snew')

# Uniform groups: ensure all columns in same group have uniform spacing
root.grid_columnconfigure(0, weight=1, uniform='group1')
root.grid_columnconfigure(1, weight=1, uniform='group1')
root.grid_rowconfigure(1, weight=1)

#cash_label.text

def buy_max(price):
    global cash
    global shares
    max_purchasable = cash // price
    cash -= max_purchasable*price
    shares += int(max_purchasable)
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

    # Algorithm logic
    price = close[current_time]
    if sma[current_time] >= price:
        buy_max(price)
    else:
        sell_max(price)

    # Update UI
    cash_label['text'] = f'Cash: ${cash:.2f}'
    shares_label['text'] = f'{shares} Shares'
    total_value_label['text'] = f'Total Liquid Value: ${cash+shares*price:.2f}'
    profit = cash+shares*price-initial_cash
    if profit == 0:
        profit_label['fg'] = 'black'
    elif profit > 0:
        profit_label['fg'] = 'green'
    else:
        profit_label['fg'] = 'red'
    profit_label['text'] = f'Total Profit: {"-" if profit < 0 else ""}${profit:.2f}'
    print(f'Cash: {cash:.2f} | Shares: {shares}')


# Create animination object
anim = FuncAnimation(fig, animate, interval=50, frames=range(len(close)-window), repeat=True)

# Run tkinter loop
tk.mainloop()