import os
import alpaca_trade_api as tradeapi
import discord
import datetime
from dotenv import load_dotenv

load_dotenv()

# connect to alpaca
KEY = os.getenv('ALPACA_KEY')
SECRET = os.getenv('ALPACA_SECRET')
api = tradeapi.REST(KEY, SECRET, api_version='v2')

symbls = ['SNAP','MSFT','QQQ']
lmt = 13
wkd = datetime.datetime.today().weekday()

# dictionary of supported timeframes and the number of candles to retrieve
grandict = {
    '5Min': lmt,
    '15Min': lmt,
    '30Min': lmt * 2,
    '1Hour': lmt * 4,
    '4Hour': lmt * 16,
    'day': lmt,
    'week': (lmt * 5)
}

# dictionary of proxy timeframes to support more than just the ones provided by the API
intdict = {
    '5Min': '5Min',
    '15Min': '15Min',
    '30Min': '15Min',
    '1Hour': '15Min',
    '4Hour': '15Min',
    'day': 'day',
    'week': 'day'  
}

def scanTicker(ticker: str, timeframe="All"):
    """
    Returns a discord.Embed object 
    """
    ticker = ticker.upper() # API only takes uppercase tickers
    description = ""
    
    ratio = grandict[timeframe] / lmt
    bars = reversed(api.get_barset(ticker, intdict[timeframe], limit=grandict[timeframe])[ticker])
    l13 = []
    cnt = 0
    for y in bars:
        if cnt % ratio == 0:
            l13.append(y.c)
        cnt += 1
    if findBuy(l13) == 9:
        description += '9er buy on ' + ticker + "\n"
    elif findSell(l13) == 9:
        description += '9er sell on ' + ticker + "\n"
    else:
        description = ""
    return description


def findBuy(last13) -> int:
    seq = 0
    i = 0
    while i < len(last13) - 4:
        curr = last13[i]
        fth = last13[i + 4]
        if curr < fth:
            seq += 1
        else:
            seq = 0
        i += 1
    return seq

def findSell(last13) -> int:
    seq = 0
    i = 0
    while i < len(last13) - 4:
        curr = last13[i]
        fth = last13[i + 4]
        if curr > fth:
            seq += 1
        else:
            seq = 0
        i += 1
    return seq