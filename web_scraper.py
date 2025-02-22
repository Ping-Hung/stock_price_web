import pandas as pd
import yfinance as yf
import datetime
import random
from requests.exceptions import ConnectionError
import requests
from bs4 import BeautifulSoup   # web scraping

def web_content_div(web_content: BeautifulSoup, class_path: str):
  """search all <div> tags with the specified class path"""
  web_content_div = web_content.find_all('div', {'class': class_path})
  try:
    # first row of all div tags, look for all <span> tags
    spans = web_content_div[0].find_all('span')
    texts = [span.get_text() for span in spans]
  except IndexError:
    # in case we cannot get any <span> tags
    texts = []
  return texts
  
    

# essentially an API call to yahoo finance to get html, then search <div> tags in html to find price and change
def get_real_time_price(stock_code: str):
  url: str = f'https://finance.yahoo.com/quote/{stock_code}/?p={stock_code}&.tsrc=fin-srch'
  # add a header to trick the website into thinking we are a browser
  user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
  ]

  headers = {
    "User-Agent": random.choice(user_agents),
  }

  try:
    r = requests.get(url, headers=headers)
    web_content = BeautifulSoup(r.text, 'html.parser')
    texts = web_content_div(web_content, "yf-16vvaki")  # !BUG: the encoding is automatically generated, shouldn't hardcode this
    if texts:
      price, change = texts[0], texts[1]
    else:
      price, change = [], []
  except ConnectionError:
    price, change = [], []

  return price, change

if __name__ == '__main__':
  stocks = ['NVDA', 'TSM', 'BTC-USD']
  for stock in stocks:
    print(stock)
    price, change = get_real_time_price(stock)
    print(f"price: {price}, change: {change}")