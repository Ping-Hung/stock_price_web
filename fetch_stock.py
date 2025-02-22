import pandas as pd
import yfinance as yf
  
def get_real_time_price(stock_code: str) -> tuple[float, float]:
  """use yfinance API to get real-time stock price"""
  stock = yf.Ticker(stock_code)
  price = stock.history(period='1d')['Close'].iloc[-1]
  # get the change in stock price
  open_price = stock.history(period='1d')["Open"].iloc[-1]
  change = (price - open_price) / open_price 
  
  return price, change

if __name__ == '__main__':
  stocks = ['NVDA', 'TSM', 'BTC-USD']
  for stock in stocks:
    print(stock)
    price, change = get_real_time_price(stock)
    print(f"price: {price: .2f}, change: {(change * 100): .2f}%")
  print("change := (price - open_price) / open_price")