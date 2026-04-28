import numpy as np

def one_step_tree(S, K, u, d, r, T, option_type="call"):

    # risk-neutral probability
    p = (np.exp(r*T) - d) / (u-d)

    if option_type == "call":
        
        ePayoff = p * max(S*u - K, 0) + (1-p) * max(S*d - K, 0)

    else:
        ePayoff = p * max(K - S*u, 0) + (1-p) * max(K - S*d, 0)

    discountedPrice = np.exp(-r*T) * ePayoff

    return discountedPrice