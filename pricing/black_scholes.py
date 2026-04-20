import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Price a euro call or put using BS.
    
    Args: 
        S: current stock price
        K: strike
        T: time to expiry in years
        r: risk-free rate as a decimal
        sigma: vol as a decimal
        option_type: "call" or "put", defaults to "call"
    
    Returns: 
        option price

    Raises:
        ValueError if T is negative or option_type is invalid
    """


    if T < 0:
        raise ValueError("T must be non-negative")
    if option_type not in ("call","put"):
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")

    # d1 components
    log_moneyness = np.log(S/K) 
    drift_term = (r + 0.5 * sigma**2) * T
    vol_scaling = sigma * np.sqrt(T)


    d1 = (log_moneyness + drift_term) / vol_scaling
    d2 = d1 - vol_scaling

  
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)



if __name__ == "__main__":
    call_price = black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call")
    put_price = black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="put")
    print(f"Call price: ${call_price:.4f}")
    print(f"Put price:  ${put_price:.4f}")
