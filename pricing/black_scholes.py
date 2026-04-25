import numpy as np
from scipy.stats import norm


class Option:

    def __init__(self, S, K, T, r, sigma, option_type="call"):

        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
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
            if self.S == self.K:
                return "ATM"
            else:
                return "OTM"

    @property
    def intrinsic_value(self):
        if self.option_type == "call":
            return max(self.S-self.K, 0)
        if self.option_type == "put":
            return max(self.K-self.S, 0)


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
    call = Call(S=105, K=100, T=1, r=0.05, sigma=0.2)
    print(call.moneyness)          # ITM
    print(call.intrinsic_value)    # 5
    print(call.payoff(110))        # 10
    print(call.profit(110, 5))     # 5

    put = Put(S=105, K=100, T=1, r=0.05, sigma=0.2)
    print(put.moneyness)           # OTM
    print(put.intrinsic_value)     # 0
    print(put.payoff(90))          # 10
    print(put.profit(90, 3))       # 7
