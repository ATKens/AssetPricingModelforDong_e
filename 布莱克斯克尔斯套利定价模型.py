from scipy.stats import norm
import numpy as np


# Black-Scholes formula for European call option
def black_scholes_call(S, K, r, q, T, sigma):
    """
    Computes the Black-Scholes price for a European call option.

    Parameters:
        S (float): current price of the underlying asset
        K (float): strike price of the option
        r (float): annual risk-free interest rate (as a decimal)
        q (float): annual dividend yield (as a decimal)
        T (float): time to expiration (in years)
        sigma (float): annual volatility of the underlying asset (as a decimal)

    Returns:
        float: price of the call option
    """
    # Calculate d1 and d2 components
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the call price
    call_price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    return call_price


# Parameters
S = 2.562  # current price of the underlying asset (上证50 ETF)
K = 2.6  # strike price
r = 0.0231  # annual risk-free interest rate (converted to decimal)
q = 0.01621  # annual dividend yield (converted to decimal)
T = 0.126  # time to expiration in years
sigma = 0.11  # annual volatility

# Calculate the call option price using the Black-Scholes model
call_option_price = black_scholes_call(S, K, r, q, T, sigma)
print('此欧式看涨期权的理论价格:',call_option_price)
