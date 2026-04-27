def bull_call_spread_payoff(S_T, K1, K2):
    """
    Payoff of a bull call spread at expiry.
    
    Args:
        S_T: stock price at expiry
        K1: lower strike
        K2: higher strike
    
    Returns:
        payoff at expiry
    """

    long_call = max(S_T - K1, 0)
    short_call = max(S_T - K2, 0)
    return long_call - short_call

def bear_put_spread_payoff(S_T, K1, K2):
    """
    Payoff of a bear put spread at expiry.
    
    Args:
        S_T: stock price at expiry
        K1: lower strike 
        K2: higher strike 
    
    Returns:
        payoff at expiry
    """

    long_put = max(K2 - S_T, 0)
    short_put = max(K1 - S_T, 0)
    return long_put - short_put

def long_straddle_payoff(S_T, K):
    """
    Payoff of a long straddle at expiry.
    
    Args:
        S_T: stock price at expiry
        K: strike price
    
    Returns:
        payoff at expiry
    """

    long_call = max(S_T - K, 0)
    long_put = max(K - S_T, 0)
    return long_call + long_put


if __name__ == "__main__":
    print("=== Bull Call Spread ===")
    print(f"S_T=40, K1=50, K2=60: {bull_call_spread_payoff(40, 50, 60)}")
    print(f"S_T=55, K1=50, K2=60: {bull_call_spread_payoff(55, 50, 60)}")
    print(f"S_T=70, K1=50, K2=60: {bull_call_spread_payoff(70, 50, 60)}")

    print("\n=== Bear Put Spread ===")
    print(f"S_T=40, K1=50, K2=60: {bear_put_spread_payoff(40, 50, 60)}")
    print(f"S_T=55, K1=50, K2=60: {bear_put_spread_payoff(55, 50, 60)}")
    print(f"S_T=70, K1=50, K2=60: {bear_put_spread_payoff(70, 50, 60)}")

    print("\n=== Long Straddle ===")
    print(f"S_T=40, K=50: {long_straddle_payoff(40, 50)}")
    print(f"S_T=50, K=50: {long_straddle_payoff(50, 50)}")
    print(f"S_T=60, K=50: {long_straddle_payoff(60, 50)}")