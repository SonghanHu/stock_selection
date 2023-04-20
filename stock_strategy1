import pandas as pd
import yfinance as yf

class stock_selection:

    def __init__(self, day_range) -> None:

        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        self.ticker = list(sp500[0]['Symbol'])
        self.day = day_range
        self.long = [], self.short = []

    def simple_strategy(self):

        data = {}
        semi = {}

        try:
            for i in range(len(self.ticker)):
                da = yf.Ticker(self.ticker[i])
                da1 = [self.ticker[i]] = da.history(period = '1mo').iloc[-self.day:,[0,3]]
                data[self.ticker[i]] = (da1.iloc[0,0],da1.iloc[-1,1])
                rate = (data[self.ticker[i]][1] - data[self.ticker[i]][0]) / data[self.ticker[i]][0]
                semi[self.ticker[i]] = rate
                
        except Exception:
            pass

        indicator = sorted(semi.items(), key = lambda item: -item[1])
        self.long = [i[0] for i in indicator[:20]]
        self.short = [i[0] for i in indicator[-20:]]
