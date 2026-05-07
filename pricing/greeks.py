from black_scholes import d1, d2, validate_black_scholes_inputs
import numpy as np
from scipy.stats import norm

def delta(S, K, T, r, sigma, option_type):

    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    d1_val = d1(S, K, T, r, sigma)

    call_delta = norm.cdf(d1_val)
    put_delta = norm.cdf(d1_val) - 1

    if option_type == 'call':
        return call_delta
    else:
        return put_delta
    
def gamma(S, K, T, r, sigma):

    # option_type does not affect gamma; passed only for validation
    validate_black_scholes_inputs(S, K, T, sigma, option_type='call')

    d1_val = d1(S, K, T, r, sigma)

    return norm.pdf(d1_val) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, sigma):

    # option_type does not affect vega; passed only for validation
    validate_black_scholes_inputs(S, K, T, sigma, option_type='call')

    d1_val = d1(S, K, T, r, sigma)

    # division by 100 to show price change per 1% change in IV
    vega = S * norm.pdf(d1_val) * np.sqrt(T) / 100

    return vega

def rho(S, K, T, r, sigma, option_type):

    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    d2_val = d2(S, K, T, r, sigma)

    # division by 100 to show price change per 1% change in interest rates
    call_rho = K * T * np.exp(-r * T) * norm.cdf(d2_val) / 100
    put_rho = -K * T * np.exp(-r * T) * norm.cdf(-d2_val) / 100

    if option_type == 'call':
        return call_rho
    else:
        return put_rho

def theta(S, K, T, r, sigma, option_type):

    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)

    vol_decay_term = (S * norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
    
    call_interest_rate_carry_term = r * K * np.exp(-r * T) * norm.cdf(d2_val)
    put_interest_rate_carry_term = r * K * np.exp(-r * T) * norm.cdf(-d2_val)

    annual_call_theta = -vol_decay_term - call_interest_rate_carry_term
    annual_put_theta = -vol_decay_term + put_interest_rate_carry_term

    daily_call_theta = annual_call_theta / 365
    daily_put_theta = annual_put_theta / 365

    if option_type == 'call':
        return daily_call_theta
    else: 
        return daily_put_theta

if __name__ == "__main__":
    print(f"Call delta: {delta(100, 100, 1, 0.05, 0.2, 'call'):.4f}")
    print(f"Put delta: {delta(100, 100, 1, 0.05, 0.2, 'put'):.4f}")
    print(f"Gamma: {gamma(100, 100, 1, 0.05, 0.2):.4f}")
    print(f"Vega: {vega(100, 100, 1, 0.05, 0.2):.4f}")
    print(f"Call rho: {rho(100, 100, 1, 0.05, 0.2, 'call'):.4f}")
    print(f"Put rho: {rho(100, 100, 1, 0.05, 0.2, 'put'):.4f}")
    print(f"Call theta: {theta(100, 100, 1, 0.05, 0.2, 'call'):.4f}")
    print(f"Put theta: {theta(100, 100, 1, 0.05, 0.2, 'put'):.4f}")