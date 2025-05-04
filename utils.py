import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

FAANG_TICKERS = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL', 'TSLA']

def get_faang_daily_returns():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5)  # Get last few days to ensure at least 2 valid trading days

    data = yf.download(FAANG_TICKERS, start=start_date, end=end_date)['Adj Close']
    data = data.dropna()

    if data.shape[0] < 2:
        raise ValueError("Not enough data to compute returns")

    latest = data.iloc[-1]
    previous = data.iloc[-2]

    returns = ((latest - previous) / previous).round(4).to_dict()
    return returns
