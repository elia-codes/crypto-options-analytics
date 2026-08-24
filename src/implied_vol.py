from black_scholes import black_scholes, vega

def implied_volatility(market_price, S, K, T, r, option_type,
                       guess=0.5, tolerance=1e-6, max_iterations=100):

    intrinsic = max(0.0, S - K) if option_type == "call" else max(0.0, K - S)
    extrinsic = market_price - intrinsic

    if T <= 0 or extrinsic <= 0.01:
        return float("nan")

    sigma = guess

    for i in range(max_iterations):
        price = black_scholes(S, K, T, r, sigma, option_type)
        error = price - market_price

        if abs(error) < tolerance:
            return sigma

        v = vega(S, K, T, r, sigma)
        if v < 1e-8:
            return float("nan")

        sigma = sigma - error / v

        if sigma <= 0:
            return float("nan")

    return float("nan")