# Why √(2π) sits in the bell curve

Fill in each box in your own words. If you can't, reread that step.

---

**1. The function**

```
e^(−x²/2)
```

Why do substitution, parts, and partial fractions all fail here?

> 

---

**2. Name the quantity**

```
I = ∫ e^(−x²) dx        from −∞ to ∞
```

What can we find, even though the antiderivative doesn't exist?

> 

---

**3. The trick**

```
I² = ( ∫ e^(−x²) dx ) · ( ∫ e^(−y²) dy )
   = ∫∫ e^(−x² − y²) dx dy
```

What was done to the original integral, and why is the second copy written in y?

> 

What does this double integral represent geometrically?

> 

---

**4. Switch to polar**

```
x² + y² = r²

dx dy  →  r dr dθ
```

Why is polar the natural choice for this particular surface?

> 

Where does the extra `r` come from, geometrically?

> 

---

**5. Now it's solvable**

```
∫ r · e^(−r²) dr
```

Which Calc II technique works here, and why didn't it work in step 1?

> 

---

**6. The result**

```
I² = π        →      I = √π

for e^(−x²/2):        I = √(2π)
```

Why does √(2π) appear as a divisor in the normal pdf?

> 

---

**7. The catch**

`N(x)` is the area from −∞ up to **one specific x**, not the whole line.

Why doesn't the polar trick work for a partial area?

> 

So how does `norm.cdf(x)` actually produce a number?

> 

---

**8. Tie it back to the code**

Black-Scholes contains two things that cannot be solved algebraically. Name both,
and say how each is handled.

> 1.

> 2.

---

**One-line summary — write it yourself:**

> 
