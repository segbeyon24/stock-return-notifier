import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

#FAANG_TICKERS = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL', 'TSLA']
FAANG_TICKERS = 'GOOGL'

def get_last_weekday():
    today = datetime.today()
    if today.weekday() == 5:      # Saturday
        return today - timedelta(days=1)
    elif today.weekday() == 6:    # Sunday
        return today - timedelta(days=2)
    else:
        return today

def get_faang_daily_returns():
    today = datetime.today()
    is_weekend = today.weekday() >= 5

    effective_day = get_last_weekday()
    start_date = effective_day - timedelta(days=14)
    end_date = effective_day + timedelta(days=1)

    try:
        data = yf.download(FAANG_TICKERS, start=start_date, end=end_date, progress=False)['Adj Close']
        data = data.dropna()
    except Exception as e:
        raise RuntimeError(f"Failed to download stock data: {e}")

    if data.shape[0] < 2:
        raise ValueError("Not enough data to compute returns")

    latest = data.iloc[-1]
    previous = data.iloc[-2]
    returns = ((latest - previous) / previous).round(4).to_dict()

    result = {
        "returns": returns,
        "effective_date": effective_day.strftime('%Y-%m-%d'),
        "note": None
    }

    if is_weekend:
        result["note"] = f"Today is {today.strftime('%A')}, not a market day. Displaying results from Friday: {effective_day.strftime('%A')}."

    return result
