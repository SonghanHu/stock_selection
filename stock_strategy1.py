import pandas as pd
import yfinance as yf

class Strategy:

    def __init__(self, ticker_list, start_date, end_date, day_range = 1):

        self.ticker_list = ticker_list
        self.day_range = day_range
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.load_data()
        self.ticker = list(self.data.keys())

    def load_data(self):
        data = {}
        for ticker in self.ticker_list:
            data[ticker] = yf.download(ticker, start=self.start_date, end=self.end_date)
        return data

    def simple_strategy(self, current_date):

        data = {}
        semi = {}

        for i in range(len(self.ticker)):
            da = self.data[self.ticker[i]].loc[pd.Timestamp(current_date) - pd.DateOffset(days=self.day_range):current_date, ['Open', 'Close']]
            
            if len(da) == 0:
                continue

            data[self.ticker[i]] = (da.iloc[0,0],da.iloc[-1,1])
            if (data[self.ticker[i]][0] > 2) & (data[self.ticker[i]][1] > 2):
                rate = (data[self.ticker[i]][1] - data[self.ticker[i]][0]) / data[self.ticker[i]][0]
                semi[self.ticker[i]] = rate

        self.indicator = sorted(semi.items(), key = lambda item: -item[1])
        self.short = [i[0] for i in self.indicator[:20]]
        self.long = [i[0] for i in self.indicator[-20:]][::-1] 
        self.short_weight = [1/40] * 20
        self.long_weight = [1/40] * 20
