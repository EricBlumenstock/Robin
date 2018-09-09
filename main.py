from Robinhood.Robinhood import Robinhood
from alpha_vantage.techindicators import TechIndicators
from sys import argv
import settings

rh = Robinhood()
ti = TechIndicators(key=settings.alphavantage_key)
stocksymbols = [str(i) for i in argv[1:]]

def main():
    quotes = []
    for i in stocksymbols:
        quotes.append(Symbol(i))

    for q in quotes:
        print(q.table())

class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol
        self.sma_short_time=10
        self.sma_long_time=60
        self.rsi_time=10
        self.quote = None
        self.LTP = None
        self.ask_price = None
        self.bid_price = None
        self.ask_size = None
        self.bid_size = None
        self.macd = None
        self.macd_computed = None
        self.rsi = None
        self.refresh()

    def refresh(self):
        self.quote = rh.quote_data(self.symbol)
        self.LTP = self.quote['last_trade_price']
        self.ask_price = self.quote['ask_price']
        self.bid_price = self.quote['bid_price']
        self.ask_size = str(self.quote['ask_size'])
        self.bid_size = str(self.quote['bid_size'])
        self.macd = self.call_macd()
        self.macd_computed = self.computed_macd_signal_diff()
        self.rsi = self.call_rsi(self.rsi_time)

    def call_sma(self, timeperiod) -> float:
        return [i['SMA'] for i in ti.get_sma(symbol=self.symbol, interval='1min', time_period=str(timeperiod))[0].values()][0]

    def call_macd(self) -> {}:
        macd = [i for i in ti.get_macd(symbol=self.symbol, interval='1min',fastperiod=12, slowperiod=26, signalperiod=9)[0].values()][0]
        return macd

    def call_rsi(self, timeperiod) -> float:
        rsi = [i['RSI'] for i in ti.get_rsi(symbol=self.symbol, interval='1min', time_period=str(timeperiod))[0].values()][0]
        return rsi
    
    def computed_macd_signal_diff(self) -> float:
        return abs((float(self.macd['MACD_Signal'])) - abs(float(self.macd['MACD'])))

    def table(self) -> str:
        return 'Symbol: {symbol}\r\nLTP: {ltp}\r\nSell: {ask_price} ({ask_size})\r\nBuy: {bid_price} ({bid_size})\r\nMACD: {macddiff}\r\nRSI: {rsi}'\
            .format(symbol=self.symbol, ltp=self.LTP, ask_price=self.ask_price, ask_size=self.ask_size,
            bid_price=self.bid_price, bid_size=self.bid_size, macddiff=self.macd_computed, rsi=self.rsi)


if __name__ == '__main__':
    main()