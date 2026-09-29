# Crypto Options Analytics Engine

A pricing and implied-volatility engine for Bitcoin options, built in
Python against Deribit's live market data.

I built this to understand how options are actually priced. It pulls around 800 live BTC contracts from Deribit, and using Black-Scholes, the code solves backwards for implied volatility. It was nice to prove myself that the Black-Scholes constant volatility assumption fails in real market and to plot the implied volatility. 

---

## What it does

1. **Pulls the live BTC option chain** from Deribit's public API, around 800
   contracts across every strike and expiry, plus current spot and the full book
   summary (bid, ask, mark, and Deribit's own mark IV).
2. **Merges** contract definitions with live prices into a single table, and
   derives time to expiry in years and moneyness (strike / spot).
3. **Prices every contract** with Black-Scholes.
4. **Solves for implied volatility** numerically using Newton-Raphson, with vega
   as the derivative.
5. **Plots the volatility smile**, implied volatility against moneyness for a
   single expiry.

## Results

**Validation.** Feeding Deribit's published `mark_iv` into the pricer reproduces
their mark prices to within a fraction of a percent. Solving in the other
direction, market price to implied volatility, recovers Deribit's IV to within
a few hundredths of a volatility point near the money.

**The smile.** Implied volatility is not constant across strikes, which directly
contradicts the assumption Black-Scholes is built on:

| Moneyness | Implied volatility |
|---|---|
| 0.971 | 59.96% |
| 0.984 | 51.67% |
| 0.997 | 49.32% |
| 1.010 | 53.47% |
| 1.016 | 56.85% |

Lowest at the money, rising on both sides. The market prices fatter tails than a
lognormal distribution allows, and since sigma is the model's only free
parameter, the excess volatility in the wings is what that mispricing costs.

**An open question.** Calls and puts at the same strike should imply identical
volatility by put-call parity, and Deribit's marks do. Solved independently,
mine diverge by 1-3 points, with calls consistently above puts. The likely cause
is the forward: Deribit options are coin-settled and priced off the forward
rather than spot. Not yet resolved.

## Used

Python · pandas · SciPy · matplotlib · requests

## Running it

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python src/deribit_API_fetch.py   # fetch, price, solve, save to data/
python src/plot_smile.py          # plot the smile
```

No API key needed, Deribit's market data endpoints are public.

## Structure

```
src/
  deribit_API_fetch.py   fetch, merge, price, solve, save
  black_scholes.py       pricing formula, vega
  implied_vol.py         Newton-Raphson solver
  plot_smile.py          volatility smile chart
data/                    generated CSVs (not tracked)
notes/                   working notes
FORMULAS.md              every formula, with what each term means
GLOSSARY.md              terminology, from terminals to implied volatility
ROADMAP.md               build plan
```

## Roadmap

- [ ] Bid/ask implied volatility band, to show where the smile is trustworthy
- [ ] Realized vs implied volatility, measuring the variance risk premium
- [ ] Resolve the call/put IV divergence (forward pricing, coin settlement)
- [ ] C++ pricing core with Python bindings for tick-level repricing
- [ ] Live WebSocket feed so the surface updates in real time
- [ ] Web dashboard: surface, smile, term structure

## Notes

This is a learning project, built to understand options pricing rather than to
trade. Implied volatility is a restatement of the market's price, not a forecast
of it, the interesting part is not the number but where the model that produces
it stops working.
