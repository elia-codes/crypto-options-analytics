import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/btc_options_with_prices.csv")

#pick one expiry

expiries = sorted(df["expiry"].unique())
print (expiries)

chosen = expiries[2]
chosen = expiries[6]
chosen = expiries[-1]

one = df[df["expiry"] == chosen]

# out-of-the-money only: calls above spot, puts below

otm = one[
    ((one["option_type"]=="call") & (one["moneyness"] > 1))
    | ((one["option_type"] == "put") & (one["moneyness"] <= 1))
]

otm = otm[(otm["moneyness"] > 0.7) & (otm["moneyness"] < 1.4)]
otm = otm.sort_values("moneyness")

plt.figure(figsize=(10, 6))
plt.plot(otm["moneyness"], otm["mark_iv"], "o-", label="Deribit mark IV")
plt.plot(otm["moneyness"], otm["my_iv"], "x--", label="My IV")
plt.axvline(1.0, color="gray", linestyle=":", label="at the money")

plt.xlabel("Moneyness  (strike / spot)")
plt.ylabel("Implied volatility  (%)")
plt.title(f"BTC volatility smile — expiry {chosen}")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig("data/smile.png", dpi=150)
plt.show()
