import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf
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

sp500 = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BBWI', 'BAX', 'BDX', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BF.B', 'CHRW', 'COG', 'CDNS', 'CZR', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CERN', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ENPH', 'ETR', 'EOG', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GNRC', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HAL', 'HBI', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HBAN', 'HII', 'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY', 'J', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NOV', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PENN', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PTC', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TWTR', 'TYL', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'UNM', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VIAC', 'VTRS', 'V', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']

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