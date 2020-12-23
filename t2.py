""" TODO:

1. Search info in google about finance trading - traingdview (RSI and MACD Strategies)
these are two technical indicators For Buy or sell signals for any stocks
2. RSI buy signal is when RSI value is less then 30 and Sell signal when more then 70

"""
from datetime import datetime

import pandas as pd
import talib as tb
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


class StrategyRSIMACD:

    def __init__(self):
        # self.ta = self.ta
        self.name = self.name
        self.data = self.data
        self.period = self.period
        self.value = self.value
        self.close = self.close

        self.rsiBuy = self.rsiSell
        self.rsiSell = self.rsiSell
        self.rsiEntry = self.rsiEntry(int)
        self.writeCatalog = self.writeCatalog
        self.loadBar = self.loadBar
        self.initDays = self.initDays
        self.onBar = self.onBar
        self.putEvent = self.putEvent()

    def __str__(self) -> str:
        return 'RSI(data=%s, period=%s)' % (self.data, self.period)

    def __dir__(self):
        return StrategyRSIMACD.__mro__

    def on_init(self):

        self.writeCatalog(u'Strategy' % self.name)

        # buy signal
        self.rsiBuy = 30 + self.rsiEntry

        # sell signal
        self.rsiSell = 70 - self.rsiEntry

        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)

        self.putEvent()

    def rsi(prices: np.ndarray, timeperiod: int = 12) -> np.ndarray:

        rsi = tb.RSI(prices, timeperiod=timeperiod)
        delta = np.r_[np.nan, np.diff(rsi)]
        return np.c_[rsi, delta]

    def macd(prices: np.ndarray, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> np.ndarray:

        macd, signal, hist = tb.MACD(prices,
                                     fastperiod=fastperiod,
                                     slowperiod=slowperiod,
                                     signalperiod=signalperiod)
        hist = (macd - signal) * 2
        delta = np.r_[np.nan, np.diff(hist)]
        return np.c_[macd, signal, hist, delta]

    def annotate_data(self, feed) -> list:

        # Get MACD
        feed['macd'], _, feed['macd_hist'] = tb.MACD(
            feed['closeMid'].values,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )

        # Get RSI
        feed['rsi'] = tb.RSI(feed['closeMid'].values)
        return feed

    def technical_indicators_df(self, daily_data):
        # googled this data, actually i can't get it how it works
        op = daily_data['Open'].values
        cls = daily_data['Close'].values
        heigh = daily_data['High'].values
        low = daily_data['Low'].values

        # building plot scenario with coordinates values and signals
        ta = pd.DataFrame()
        ta['MACD'] = tb.MACD(cls, fastperiod=12, slowperiod=26, signalperiod=9)[0] / \
                     tb.MACD(cls, fastperiod=12, slowperiod=26, signalperiod=9)[0].mean()
        ta['RSI'] = tb.RSI(cls, timeperiod=14) / tb.RSI(cls, timeperiod=14).mean()

        ta["High/Open"] = heigh / op
        ta["Low/Open"] = low / op
        ta["Close/Open"] = cls / op

    def results(self, data_frame):
        try:
            data_frame[self.value] = tb.RSI(data_frame[self.data].values, timeperiod=self.period)

            wins = 80
            ### rsi

            plt.subplot2grid((8, 1), (5, 0))
            plt.plot(self.rsi[-wins:], color='black', lw=1)
            plt.axhline(y=30, color='red', linestyle='-')
            plt.axhline(y=70, color='blue', linestyle='-')

            ## MACD

            plt.subplot2grid((8, 1), (6, 0))

            plt.plot(self.macd[-wins:], 'blue', lw=1)

            plt.subplot2grid((8, 1), (7, 0))

            plt.axhline(y=0, color='b', linestyle='-')

            plt.show()

        except KeyError:
            data_frame[self.value] = np.nan


if __name__ == '__main__':
    now = datetime.today().strftime('%Y-%m-%d')
    ticker = ['AAPL', 'FB', 'AMZN', ]

    # Download sample data
    dataset = yf.download(ticker[0], '2020-1-1', now)

    test_rsi = StrategyRSIMACD().results(dataset)