# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 23:47:02 2024

@author: Yunus
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download Bitcoin data
btc_data = yf.download("BTC-USD", start="2015-01-01")

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate RSI and add it to the DataFrame
btc_data['RSI'] = calculate_rsi(btc_data)

# Define thresholds for speculative behavior
btc_data['Speculative_Bubble'] = np.where(btc_data['RSI'] > 70, 1, 0)

# Plot Close Prices and Speculative Bubbles
plt.figure(figsize=(14, 7))
plt.plot(btc_data.index, btc_data['Close'], label='Bitcoin Price')
plt.scatter(btc_data.index, btc_data['Close'] * btc_data['Speculative_Bubble'], color='red', label='Speculative Bubbles')
plt.title('Bitcoin Price and Speculative Bubble Detection (Greater Fool Theory)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Analyze periods with speculative bubbles
bubble_periods = btc_data[btc_data['Speculative_Bubble'] == 1]
print(f"Number of speculative bubble periods detected: {len(bubble_periods)}")
