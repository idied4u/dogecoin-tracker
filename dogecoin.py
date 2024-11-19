import requests
import pandas as pd
import datetime
import os
import uuid

def fetch_dogecoin_data():
    # Fetch historical market data from CoinGecko API
    url = "https://api.coingecko.com/api/v3/coins/dogecoin/market_chart"
    params = {"vs_currency": "usd", "days": "30", "interval": "daily"}  # 30 days of data
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

def calculate_fibonacci_levels(prices):
    high = max(prices)
    low = min(prices)
    diff = high - low
    return {
        "0%": low,
        "23.6%": high - 0.236 * diff,
        "38.2%": high - 0.382 * diff,
        "50%": (high + low) / 2,
        "61.8%": high - 0.618 * diff,
        "100%": high
    }

def calculate_rsi(prices, period=14):
    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    gains = sum(delta for delta in deltas if delta > 0)
    losses = abs(sum(delta for delta in deltas if delta < 0))
    if losses == 0:  # To prevent division by zero
        return 100
    rs = gains / losses
    return 100 - (100 / (1 + rs))

def fractal_analysis(prices):
    fractals = []
    for i in range(2, len(prices) - 2):
        if prices[i - 2] < prices[i] > prices[i + 2]:
            fractals.append((i, "High"))
        if prices[i - 2] > prices[i] < prices[i + 2]:
            fractals.append((i, "Low"))
    return fractals

def make_recommendation(rsi, current_price, fib_levels):
    if rsi < 30 and current_price < fib_levels["38.2%"]:
        return "Buy"
    elif rsi > 70 and current_price > fib_levels["61.8%"]:
        return "Sell"
    else:
        return "Hold"

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Main script
try:
    data = fetch_dogecoin_data()
    prices = [point[1] for point in data["prices"]]
    timestamps = [datetime.datetime.fromtimestamp(point[0] / 1000).strftime('%Y-%m-%d') for point in data["prices"]]
    current_price = prices[-1]

    # Technical Analysis
    fib_levels = calculate_fibonacci_levels(prices)
    rsi = calculate_rsi(prices)
    fractals = fractal_analysis(prices)
    recommendation = make_recommendation(rsi, current_price, fib_levels)

    # Prepare CSV data
    csv_data = {
        "Date": timestamps,
        "Price": prices,
        "RSI": [rsi] * len(prices),
        "Fibonacci Levels": [fib_levels] * len(prices),
        "Recommendation": [recommendation] * len(prices)
    }
    unique_filename = f"dogecoin_analysis_{uuid.uuid4().hex}.csv"
    save_to_csv(csv_data, unique_filename)

    print(f"Analysis complete. Data saved to {unique_filename}.")
    print(f"Recommendation: {recommendation}")

except Exception as e:
    print(f"Error: {e}")
