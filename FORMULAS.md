# Black-Scholes: formula reference

Every formula behind the pricing code, with what each one is for.

---

## 1. The symbols

| Symbol | Name | Where yours comes from |
|---|---|---|
| **S** | spot price of the underlying | `underlying_price` column |
| **K** | strike price | `strike` column |
| **T** | time to expiry, **in years** | `time_to_expiry` column |
| **r** | risk-free rate, annualised | `0.0` for crypto |
| **σ** (sigma) | volatility, annualised, as a decimal | `mark_iv / 100` |
| **C, P** | call price, put price | what you're solving for |

---

## 2. Payoff at expiry (intrinsic value)

```
Call payoff = max(S − K, 0)
Put  payoff = max(K − S, 0)
```

What the option is worth on the final day. No model needed — pure subtraction.
This is also the `T <= 0` guard clause in your code.

---

## 3. Premium = intrinsic + extrinsic

```
Intrinsic = max(S − K, 0)          for a call
Extrinsic = premium − intrinsic
```

Intrinsic is what you'd make exercising now. Extrinsic (time value) is what the
remaining *possibility* is worth.

**Black-Scholes outputs the total premium — intrinsic and extrinsic together.**
The intrinsic part is trivial subtraction; the extrinsic part is the only bit that
needs a model. So deep in-the-money options (nearly all intrinsic) are a weak test
of the code, and at-the-money options (nearly all extrinsic) are a strong one.

---

## 4. Expected movement

```
σ√T
```

How far the underlying is expected to wander between now and expiry, as a fraction
of spot. The single most important quantity in the whole model.

Note the **square root**: randomness accumulates with √time, not time. Four times
as long gives twice the expected movement, not four times.

Example: σ = 60%, T = 0.12 years → 0.60 × 0.346 = **20.8%**

---

## 5. d1 and d2 — standardised distance

```
d1 = [ ln(S/K) + (r + σ²/2)·T ] / (σ√T)

d2 = d1 − σ√T
```

These are **z-scores**: how far the strike is from spot, measured in units of
expected movement.

- `ln(S/K)` — log-moneyness, the distance from spot to strike
- `σ√T` — the unit of measurement (from §4)
- `σ²/2` — a correction for the lognormal distribution's skew

---

## 6. N(·) — the normal CDF

```
N(x) = probability a standard normal draw is below x
```

Converts a z-score into a probability. In code: `norm.cdf(x)` from scipy.

**N(d2) ≈ the probability the option finishes in the money** (under the
risk-neutral measure — it is not a real-world forecast).

---

## 7. The pricing formulas

```
Call = S·N(d1) − K·e^(−rT)·N(d2)

Put  = K·e^(−rT)·N(−d2) − S·N(−d1)
```

Read as **what you get minus what you pay**:

- `S·N(d1)` — expected value of receiving the asset, if you exercise
- `K·e^(−rT)·N(d2)` — expected cost of paying the strike, discounted to today

`e^(−rT)` is discounting. With **r = 0** it equals 1 and drops out entirely.

---

## 8. Put-call parity

```
C − P = S − K·e^(−rT)
```

A no-arbitrage identity: a call minus a put at the same strike and expiry equals
the underlying minus the discounted strike. Violate it and there's riskless profit.

**Consequence:** a call and a put at the same strike must imply the **same
volatility**. That's why your 58,000 call and put both showed `mark_iv` 60.25.

Also a free check on your code: compute both and confirm the identity holds.

---

## 9. The Greeks — sensitivities

Each answers "how much does the premium change when one input moves?"

**Two symbols, kept strictly apart:**

```
N(x)  =  norm.cdf(x)    the AREA under the bell curve up to x — a probability
φ(x)  =  norm.pdf(x)    the HEIGHT of the bell curve at x — a density
```

Delta uses `N` (cdf). Vega, gamma and theta use `φ` (pdf) — because they are
derivatives of the price, and differentiating an area gives back a height.

```
Delta   call:  N(d1)
        put:   N(d1) − 1
```
Change in premium per $1 change in spot. Also the amount of the underlying you'd
hold to hedge. Ranges 0→1 for calls, −1→0 for puts.

```
Gamma   φ(d1) / (S·σ·√T)
```
Change in **delta** per $1 change in spot. How fast your hedge goes stale.
Same for calls and puts.

```
Vega    S·φ(d1)·√T
```
Change in premium per 1.00 change in σ (divide by 100 for "per 1 vol point").
Same for calls and puts. **This is the derivative Newton-Raphson uses.**

```
Theta   call:  −S·φ(d1)·σ/(2√T) − r·K·e^(−rT)·N(d2)
        put:   −S·φ(d1)·σ/(2√T) + r·K·e^(−rT)·N(−d2)
```
Change in premium per year of time passing. Usually negative — options decay.
Divide by 365 for daily decay.

```
Rho     call:   K·T·e^(−rT)·N(d2)
        put:   −K·T·e^(−rT)·N(−d2)
```
Sensitivity to interest rates. Near-irrelevant for crypto, where r = 0.

---

## 10. Implied volatility — Newton-Raphson

Black-Scholes runs σ → price. There is **no algebraic inverse**, so to get
price → σ you iterate:

```
σ(n+1) = σ(n) − [ BS(σ(n)) − market_price ] / vega(σ(n))
```

- start at a guess, e.g. σ = 0.5
- compute the model price and how far off it is
- divide the error by vega (the slope) to get the correction
- repeat until the error is tiny, typically 3–5 rounds

Stop when `|BS(σ) − market| < 0.0001` or after ~100 iterations.

**Watch out:** vega approaches zero for deep in- or out-of-the-money options,
which makes the correction explode. Guard against it.

---

## 11. Unit conventions — where bugs come from

| Thing | Convention | The bug |
|---|---|---|
| σ | decimal (0.6025) | Deribit gives `60.25` — divide by 100 |
| T | years | days gives prices ~20× too high |
| Time zone | UTC | `pd.Timestamp.now()` is local — use `utcnow()` |
| Deribit prices | quoted in **BTC** | multiply by `underlying_price` for USD |
| r | 0 for crypto | Deribit's own `interest_rate` field is 0.0 |

---

## 12. Formula → your code

```python
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)     # call
price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)   # put
```

| Maths | Python |
|---|---|
| ln(x) | `np.log(x)` |
| √x | `np.sqrt(x)` |
| e^x | `np.exp(x)` |
| σ² | `sigma**2` |
| N(x) | `norm.cdf(x)` |
| φ(x) | `norm.pdf(x)` |

---

## 13. What the model assumes — and why the smile exists

Black-Scholes assumes:

1. Volatility is **constant** across strikes and time
2. Prices move **smoothly**, no jumps
3. Returns are **lognormal**
4. Continuous trading, no transaction costs

All four are false. The first is falsifiable with your own data: if σ were a
property of Bitcoin, every strike would imply the same number. Yours don't —

```
58,000 → 60.25      59,000 → 55.53      60,000 → 54.79
```

That's the **volatility smile**. Markets price crash risk higher than a lognormal
distribution implies, so far-from-the-money options cost more than the model says.

So Black-Scholes is used as a **translation layer**, not a truth machine: a way to
convert prices into a comparable unit (IV), the same way bond prices are quoted as
yields. Plotting where it breaks is the actual information.
