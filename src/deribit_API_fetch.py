import requests
import pandas as pd

r = requests.get(
    "https://www.deribit.com/api/v2/public/get_instruments",
    params={"currency": "BTC", "kind": "option", "expired": "false"}
)

rows = r.json()["result"]

print(len(rows))

df = pd.DataFrame(rows)
df = df[["instrument_name", "strike", "option_type", "expiration_timestamp"]]
df["expiry"] = pd.to_datetime(df["expiration_timestamp"], unit="ms")
print(df.head())
df.to_csv("data/btc_options.csv", index=False)
