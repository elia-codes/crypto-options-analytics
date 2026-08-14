import requests
import pandas as pd

# Fetch BTC options data from Deribit API
response_instruments = requests.get(
    "https://www.deribit.com/api/v2/public/get_instruments",
    params={"currency": "BTC", "kind": "option", "expired": "false"}
)

response_spot = requests.get(
    "https://www.deribit.com/api/v2/public/get_index_price",
    params={"index_name": "btc_usd"}
)

response_prices = requests.get(
    "https://www.deribit.com/api/v2/public/get_book_summary_by_currency",
    params={"currency": "BTC", "kind": "option"}
)

rows = response_instruments.json()["result"]
rows_spot = response_spot.json()["result"]
price_rows = response_prices.json()["result"]

print(len(rows))
print(len(rows_spot))
print (rows_spot)
spot = rows_spot["index_price"]
print(spot)
print(len(price_rows))
print(price_rows[0])

df = pd.DataFrame(rows)
df = df[["instrument_name", "strike", "option_type", "expiration_timestamp"]]
df["expiry"] = pd.to_datetime(df["expiration_timestamp"], unit="ms")
print(df.head())

prices_df = pd.DataFrame(price_rows)
prices_df = prices_df[["instrument_name", "bid_price", "ask_price", "mark_price", "mark_iv", "underlying_price"]]
print(prices_df.head())

merged = pd.merge(df, prices_df, on="instrument_name")
merged.to_csv("data/btc_options_with_prices.csv", index=False)
print(merged.head())
print(len(merged))

#Black Scholes formula for option pricing

import numpy as np

now = pd.Timestamp.now('utc').tz_localize(None)
merged["time_to_expiry"] = (merged["expiry"] - now).dt.total_seconds() / (365 * 24 * 60 * 60)
print(merged[["instrument_name", "expiry", "time_to_expiry"]].head())

merged["mark_price_usd"]= merged["mark_price"] * merged["underlying_price"]

from black_scholes import black_scholes

merged["bs_price"] = merged.apply(
    lambda row: black_scholes(
        S=row["underlying_price"],
        K=row["strike"],
        T=row["time_to_expiry"],
        r=0.00,  # Assuming a risk-free rate of 0%
        sigma=row["mark_iv"]/100,  # Convert implied volatility from percentage to decimal
        option_type=row["option_type"]
    ), 
    axis=1
)

print(merged[["instrument_name", "strike", "option_type", "expiry", "mark_price_usd", "bs_price"]].head())