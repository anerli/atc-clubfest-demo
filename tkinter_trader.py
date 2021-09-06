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
y_height = max(close)
window = 100

# Animate function
def animate(t):
    ax.clear()
    ax.set_ylim(0, y_height+10)
    ax.plot(close[t:t+window])
    #ax.plot(close[0:t])

# Create animination object
anim = FuncAnimation(fig, animate, interval=10, frames=range(len(close)-window))

# Run tkinter loop
tk.mainloop()