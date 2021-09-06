import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import yfinance as yf

# Create tk window root
root = tk.Tk()
root.title('Automated Trader')



fig = plt.figure()



canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)





ax = fig.add_subplot()

data = yf.download('AAPL','2016-01-01','2019-08-01')
close = data['Adj Close']
y_height = max(close)

#print(y_height)
window = 100

def animate(t):
    print(t)
    ax.clear()
    ax.set_ylim(0, y_height+10)
    ax.plot(close[t:t+window])
    #ax.plot(close[0:t])

anim = FuncAnimation(fig, animate, interval=10, frames=range(len(close)-window))
#plt.show()

# fig = plt.figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))




tk.mainloop()