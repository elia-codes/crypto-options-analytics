import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type):
    """
    Calculate the Black-Scholes option price.

    Parameters:
    S : float
        Current stock price (underlying asset price)
    K : float
        Strike price of the option
    T : float
        Time to expiration in years
    r : float
        Risk-free interest rate (annualized)
    sigma : float
        Volatility of the underlying asset (annualized)
    option_type : str
        Type of the option ('call' or 'put')

    Returns:
    float
        Theoretical price of the option
    """
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K) if option_type == "call" else max(0.0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price

print(black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call"))


