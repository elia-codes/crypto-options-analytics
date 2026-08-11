# Crypto Options Analytics Engine

A tool that pulls live Bitcoin options data from Deribit, prices those options
with Black-Scholes, solves for implied volatility, and visualises the volatility
surface in real time.

**Why this project:** implied volatility has no closed-form solution. You cannot
look at a chart and see it — it has to be solved numerically. Same for the Greeks
(calculus derivatives) and the surface (a 3D object over strike x expiry that
moves every tick). This is code or nothing.

**Scope note:** analytics only. Building the tool is the goal. Trading it with
real money is a separate decision, made later, deliberately.

---

## Stack

| Layer | Language | Job |
|---|---|---|
| Data | Python | Deribit public API (REST + WebSocket) |
| Research | Python | Black-Scholes, implied vol, Greeks, pandas |
| Performance | C++ | Pricing engine, Monte Carlo, repricing on every tick |
| Glue | pybind11 | Python calls the C++ engine |
| Presentation | JS / CSS | Vol surface, smile, term structure, scanner |

---

## Week 1 — Python: get the data, price the options

- [ ] **Step 1** — First live call to Deribit. Print one BTC option's data.
- [ ] **Step 2** — `src/fetch_options.py`: pull the whole chain into pandas, save to `data/btc_options.csv`.
- [ ] **Step 3** — Options basics (call/put, strike, expiry, moneyness). Parse `BTC-26SEP26-80000-C` into columns.
- [ ] **Step 4** — Black-Scholes in Python. Test against known values.
- [ ] **Step 5** — Implied volatility via Newton-Raphson. Compare to Deribit's own IV as a check.
- [ ] **Step 6** — Plot the volatility smile: IV vs strike, one expiry.

## Week 2 — C++: the pricing engine

- [ ] Set up a compiler and build your first C++ program
- [ ] Port Black-Scholes to C++
- [ ] Monte Carlo pricer for path-dependent payoffs
- [ ] Benchmark C++ vs Python on 10,000 options

## Week 3 — Glue and go live

- [ ] pybind11: call the C++ pricer from Python
- [ ] Deribit WebSocket feed — live order book updates
- [ ] Surface recalculates in real time as quotes change

## Week 4 — Make it visible

- [ ] JSON export from Python
- [ ] 3D volatility surface (strike x expiry x IV)
- [ ] Smile per expiry, term structure of ATM vol
- [ ] Mispricing scanner: flag options whose IV is off versus neighbours
- [ ] README with screenshots, pushed to GitHub

---

## How we work

1. I explain the concept and the new syntax it needs
2. **You** write the code
3. You save; I read the file and review it like a senior dev would
4. We fix, then commit to git

Every unfamiliar line gets explained. Ask about anything — the questions about
`.` and `()` and `to_csv` were the right questions, and there will be more.

## Daily habit

```
git add -A
git commit -m "what you did today"
```

Small commits, every day. Momentum beats any single feature.
