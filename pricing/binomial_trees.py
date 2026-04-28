import numpy as np

def one_step_tree(S, K, r, T, sigma, option_type="call"):

    # risk-neutral probability
    u = np.exp(sigma * np.sqrt(T))
    d = 1/u
    p = (np.exp(r*T) - d) / (u-d)

    if option_type == "call":
        
        ePayoff = p * max(S*u - K, 0) + (1-p) * max(S*d - K, 0)

    else:
        ePayoff = p * max(K - S*u, 0) + (1-p) * max(K - S*d, 0)

    discountedPrice = np.exp(-r*T) * ePayoff

    return discountedPrice

def n_step_tree(S, K, r, T, sigma, n, option_type="call"):

    dt = T / n
    u = np.exp(sigma* np.sqrt(dt))
    d = 1/u
    p = (np.exp(r * dt) - d) / (u - d)
    
    if option_type == "call":
        payoffs = [max(S * u**j * d**(n-j) - K, 0) for j in range(n+1)]
    else:
        payoffs = [max(K - S * u**j * d**(n-j), 0) for j in range(n+1)]

    for step in range(n):
        for j in range(n - step):
            payoffs[j] = np.exp(-r * dt) * (p * payoffs[j+1] + (1-p) * payoffs[j])

    discountedPrice = payoffs[0]

    return discountedPrice


if __name__ == "__main__":
    for n in [10, 50, 100, 500]:
        price = n_step_tree(100, 100, 0.05, 1, 0.2, n, "call")
        print(f"n={n}: ${price:.4f}")
