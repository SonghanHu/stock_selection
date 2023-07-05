class Backtester:
    def __init__(self, strategy, start, end):
        
        self.strategy = strategy
        self.start = start
        self.end = end
        self.dates = pd.date_range(start, end, freq='B')

    def backtest(self):

        portfolio_value = 1000000
        prev_long_portfolio = {}
        prev_short_portfolio = {}

        portfolio_values = []

        for i in range(0, len(self.dates) - 1):
            for stock, shares in prev_long_portfolio.items():
                if self.dates[i] in self.strategy.data[stock].index:
                    portfolio_value += shares * self.strategy.data[stock].loc[self.dates[i], 'Open']

            for stock, shares in prev_short_portfolio.items():
                if self.dates[i] in self.strategy.data[stock].index:
                    portfolio_value -= shares * self.strategy.data[stock].loc[self.dates[i], 'Open']

            self.strategy.simple_strategy(self.dates[i].strftime('%Y-%m-%d'))
            new_long_portfolio = {}
            new_short_portfolio = {}

            for stock in self.strategy.long:
                if self.dates[i] in self.strategy.data[stock].index:
                    shares_to_buy = portfolio_value * self.strategy.long_weight[self.strategy.long.index(stock)] \
                                    / self.strategy.data[stock].loc[self.dates[i], 'Close']
                    new_long_portfolio[stock] = shares_to_buy
                    portfolio_value -= shares_to_buy * self.strategy.data[stock].loc[self.dates[i], 'Open']

            for stock in self.strategy.short:
                if self.dates[i] in self.strategy.data[stock].index:
                    shares_to_sell = portfolio_value * self.strategy.short_weight[self.strategy.short.index(stock)] \
                                     / self.strategy.data[stock].loc[self.dates[i], 'Close']
                    new_short_portfolio[stock] = shares_to_sell
                    portfolio_value += shares_to_sell * self.strategy.data[stock].loc[self.dates[i], 'Open']

            portfolio_values.append(portfolio_value)

            prev_long_portfolio = new_long_portfolio
            prev_short_portfolio = new_short_portfolio

        for stock, shares in prev_long_portfolio.items():
            if self.dates[len(self.dates) - 1] in self.strategy.data[stock].index:
                portfolio_value += shares * self.strategy.data[stock].loc[self.dates[len(self.dates) - 1], 'Open']

        for stock, shares in prev_short_portfolio.items():
            if self.dates[len(self.dates) - 1] in self.strategy.data[stock].index:
                portfolio_value -= shares * self.strategy.data[stock].loc[self.dates[len(self.dates) - 1], 'Open']

        return pd.DataFrame({
            'Portfolio Value': portfolio_values,
        })
