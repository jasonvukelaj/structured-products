import numpy as np
from scipy.stats import norm


class Option:

    def __init__(self, S, K, T, r, sigma, option_type="call"):

        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

        if not isinstance(option_type, str):
            raise ValueError("option_type must be a string")
        
        option_type = option_type.lower()

        if not self.is_valid_type(option_type):
            raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
        
        self.option_type = option_type

    @staticmethod
    def is_valid_type(option_type):
        return option_type in ("call", "put")

    @property
    def moneyness(self):
        if self.option_type == "call":
            if self.S > self.K:
                return "ITM"
            elif self.S == self.K:
                return "ATM"
            else:
                return "OTM"
        
        elif self.option_type == "put":
            if self.S < self.K:
                return "ITM"
            elif self.S == self.K:
                return "ATM"
            else:
                return "OTM"

    @property
    def intrinsic_value(self):
        if self.option_type == "call":
            return max(self.S - self.K, 0)
        
        elif self.option_type == "put":
            return max(self.K - self.S, 0)
        
    def __repr__(self):
        return f"{self.option_type.upper()} | S: ${self.S} K: ${self.K} T: {self.T} year(s) r: {self.r*100}% σ: {self.sigma*100}% | {self.moneyness} | IV: ${self.intrinsic_value}"
        
class Call(Option):

    def __init__(self, S, K, T, r, sigma):
        super().__init__(S, K, T, r, sigma, option_type="call")

    def payoff(self, S_T):
        return max(S_T - self.K, 0)

    def profit(self, S_T, premium):
        return self.payoff(S_T) - premium

class Put(Option):

    def __init__(self, S, K, T, r, sigma):
        super().__init__(S, K, T, r, sigma, option_type="put")

    def payoff(self, S_T):
        return max(self.K - S_T , 0)

    def profit(self, S_T, premium):
        return self.payoff(S_T) - premium


def validate_black_scholes_inputs(S, K, T, sigma, option_type):
    if S <= 0:
        raise ValueError("S must be positive")
    if K <= 0:
        raise ValueError("K must be positive")
    if T <= 0:
        raise ValueError("T must be positive")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if not isinstance(option_type, str):
        raise ValueError("option_type must be a string")
    if option_type.lower() not in ("call", "put"):
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
    
def d1(S, K, T, r, sigma):

    log_moneyness = np.log(S / K)
    drift = (r + 0.5 * sigma**2) * T
    vol_scaling = sigma * np.sqrt(T)

    return (log_moneyness + drift) / vol_scaling

def d2(S, K, T, r, sigma):

    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

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
    """

    # validator
    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()
    
    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
  
    if option_type == "call":
        return S * norm.cdf(d1_val) - K * np.exp(-r * T) * norm.cdf(d2_val)
    else:  # put
        return K * np.exp(-r * T) * norm.cdf(-d2_val) - S * norm.cdf(-d1_val)


def test_put_call_parity(S, K, T, r, sigma):

    lhs = black_scholes(S, K, T, r, sigma, option_type="call") - black_scholes(S, K, T, r, sigma, option_type="put")
    rhs = S - K * np.exp(-r * T) 

    print(f"Left side of Put-Call parity = ${lhs:.2f}")
    print(f"Right side of Put-Call parity = ${rhs:.2f}")

    if abs(lhs - rhs) < 1e-10:  # prevents potential floating-point rounding errors
        print("Put-Call Parity is True")
    else: 
        print("Put-Call Parity is False")

if __name__ == "__main__":

    c = black_scholes(100, 100, 1, 0.05, 0.2, "call")
    p = black_scholes(100, 100, 1, 0.05, 0.2, "put")

    print(f"Call price: ${c:.2f}")
    print(f"Put price: ${p:.2f}")
    test_put_call_parity(100, 100, 1, 0.05, 0.2)
