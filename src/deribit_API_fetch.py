import requests
import pandas as pd
import numpy as np
from black_scholes import black_scholes
from implied_vol import implied_volatility


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

df = pd.DataFrame(rows)
df = df[["instrument_name", "strike", "option_type", "expiration_timestamp"]]
df["expiry"] = pd.to_datetime(df["expiration_timestamp"], unit="ms")

prices_df = pd.DataFrame(price_rows)
prices_df = prices_df[["instrument_name", "bid_price", "ask_price", "mark_price", "mark_iv", "underlying_price"]]

merged = pd.merge(df, prices_df, on="instrument_name")
merged.to_csv("data/btc_options_with_prices.csv", index=False)

#Black Scholes formula for option pricing

now = pd.Timestamp.now('utc').tz_localize(None)
merged["time_to_expiry"] = (merged["expiry"] - now).dt.total_seconds() / (365 * 24 * 60 * 60)

merged["mark_price_usd"]= merged["mark_price"] * merged["underlying_price"]

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
# At the money option price is the same as the underlying price

merged["diff"]=merged["mark_price_usd"] - merged["bs_price"]

near = merged[(merged["strike"] > 62000) & (merged["strike"] < 65000)]

merged["my_iv"] = merged.apply(
    lambda row: implied_volatility(
        market_price=row["mark_price_usd"],
        S=row["underlying_price"],
        K=row["strike"],
        T=row["time_to_expiry"],
        r=0.0,
        option_type=row["option_type"],
    ) * 100,
    axis=1
)

merged["iv_diff"] = merged["my_iv"] - merged["mark_iv"]

merged["moneyness"] = merged["strike"] / merged["underlying_price"]

near = merged[(merged["moneyness"] > 0.97) & (merged["moneyness"] < 1.03)]

merged.to_csv("data/btc_options_with_prices.csv", index=False) 
print(near[["instrument_name", "moneyness", "mark_iv", "my_iv", "iv_diff"]].head(15))

