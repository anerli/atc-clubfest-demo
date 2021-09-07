import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Trader:
    def __init__(self, price_series):
        self.price = price_series


class SMATrader(Trader):
    def __init__(self, price_series, moving_average_series):
        super().__init__(price_series)
        self.ma = moving_average_series
        assert len(self.price) == len(self.ma)

    def simulate(self, initial_cash):
        # TODO: Animate
        for t in range(len(self.price)):
            pass




if __name__ == '__main__':
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)

    close = data['MSFT']
    sma20 = close.rolling(window=20).mean()
    #msft = pd.DataFrame(data={'close': close, 'sma20': sma20})
    #print(asset.head())
    trader = SMATrader(close, sma20)
