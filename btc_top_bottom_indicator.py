import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import pandas_ta as ta  # Using pandas_ta instead of talib
from datetime import datetime

# Constants
API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
PARAMS = {"vs_currency": "usd", "days": "365", "interval": "daily"}  # 2 years of data

# Fetch Bitcoin historical data
def get_btc_data():
    response = requests.get(API_URL, params=PARAMS)
    data = response.json()
    
    # Debugging step: Print the API response to inspect its structure
    print("API Response:", data)
    
    if "prices" not in data:
        raise KeyError("The API response does not contain 'prices'. Check if the API request failed or if the response format changed.")
    
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit='ms')
    return prices


# Calculate Moving Averages
def calculate_moving_averages(df):
    df['50_SMA'] = df['price'].rolling(window=50).mean()
    df['200_SMA'] = df['price'].rolling(window=200).mean()
    df['50_EMA'] = ta.ema(df['price'], length=50)
    df['200_EMA'] = ta.ema(df['price'], length=200)
    return df

# Calculate RSI
def calculate_rsi(df):
    df['RSI'] = ta.rsi(df['price'], length=14)
    return df

# Calculate MACD
def calculate_macd(df):
    macd = ta.macd(df['price'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']
    return df

# Identify Buy/Sell Signals
def identify_signals(df):
    df['Buy_Signal'] = (df['price'] < df['200_SMA']) & (df['RSI'] < 30) & (df['MACD'] > df['MACD_Signal'])
    df['Sell_Signal'] = (df['price'] > df['200_SMA']) & (df['RSI'] > 70) & (df['MACD'] < df['MACD_Signal'])
    return df

# Backtest Strategy
def backtest(df):
    balance = 10000  # Initial capital in USD
    btc_holdings = 0
    for i in range(len(df)):
        if df.loc[df.index[i], 'Buy_Signal'] and balance > 0:
            btc_holdings = balance / df.loc[df.index[i], 'price']
            balance = 0
            print(f"BUY at {df.loc[df.index[i], 'price']:.2f} on {df.loc[df.index[i], 'timestamp'].date()}")
        elif df.loc[df.index[i], 'Sell_Signal'] and btc_holdings > 0:
            balance = btc_holdings * df.loc[df.index[i], 'price']
            btc_holdings = 0
            print(f"SELL at {df.loc[df.index[i], 'price']:.2f} on {df.loc[df.index[i], 'timestamp'].date()}")
    final_balance = balance if balance > 0 else btc_holdings * df.iloc[-1]['price']
    print(f"Final Balance: ${final_balance:.2f}")

# Plot Data
def plot_data(df):
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['price'], label='BTC Price', color='black')
    plt.plot(df['timestamp'], df['50_SMA'], label='50-Day SMA', linestyle='dashed')
    plt.plot(df['timestamp'], df['200_SMA'], label='200-Day SMA', linestyle='dashed')
    plt.scatter(df['timestamp'][df['Buy_Signal']], df['price'][df['Buy_Signal']], marker='^', color='green', label='Buy', alpha=1)
    plt.scatter(df['timestamp'][df['Sell_Signal']], df['price'][df['Sell_Signal']], marker='v', color='red', label='Sell', alpha=1)
    plt.legend()
    plt.title('Bitcoin Market Top & Bottom Model')
    plt.show()

# Main Execution
if __name__ == "__main__":
    btc_data = get_btc_data()
    btc_data = calculate_moving_averages(btc_data)
    btc_data = calculate_rsi(btc_data)
    btc_data = calculate_macd(btc_data)
    btc_data = identify_signals(btc_data)
    backtest(btc_data)
    plot_data(btc_data)
