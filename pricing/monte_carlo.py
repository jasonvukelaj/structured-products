import numpy as np
import matplotlib.pyplot as plt
from black_scholes import validate_black_scholes_inputs, black_scholes

def simulate_terminal_prices(S, T, r, sigma, n_paths=100000, seed=None):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_paths)

    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    return S_T

def mc_price(S, K, T, r, sigma, option_type, n_paths=100000, seed=None):
    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    S_T = simulate_terminal_prices(S, T, r, sigma, n_paths, seed)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    price = np.exp(-r * T) * np.mean(payoffs)

    return price

def mc_standard_error(S, K, T, r, sigma, option_type, n_paths=100000, seed=None):
    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    S_T = simulate_terminal_prices(S, T, r, sigma, n_paths, seed)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    discounted_payoffs = np.exp(-r * T) * payoffs

    return np.std(discounted_payoffs, ddof=1) / np.sqrt(n_paths)

def plot_terminal_prices(S, T, r, sigma, n_paths=100000, seed=None):
    S_T = simulate_terminal_prices(S, T, r, sigma, n_paths, seed)

    plt.hist(S_T, bins=50)
    plt.xlabel("Terminal stock price")
    plt.ylabel("Frequency")
    plt.title("Monte Carlo Simulated Terminal Prices")
    plt.show()

def plot_payoffs(S, K, T, r, sigma, option_type, n_paths=100000, seed=None):
    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    S_T = simulate_terminal_prices(S, T, r, sigma, n_paths, seed)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    plt.hist(payoffs, bins=50)
    plt.xlabel("Option payoff")
    plt.ylabel("Frequency")
    plt.title(f"Simulated {option_type.capitalize()} Payoffs")
    plt.show()

def plot_convergence(S, K, T, r, sigma, option_type, path_counts, seed=None):
    validate_black_scholes_inputs(S, K, T, sigma, option_type)
    option_type = option_type.lower()

    mc_prices = []

    for n in path_counts:
        price = mc_price(S, K, T, r, sigma, option_type, n_paths=n, seed=seed)
        mc_prices.append(price)

    bs_price = black_scholes(S, K, T, r, sigma, option_type)

    plt.plot(path_counts, mc_prices, marker="o")
    plt.axhline(bs_price, linestyle="--", label="Black-Scholes price")
    plt.xlabel("Number of simulations")
    plt.xscale("log")
    plt.ylabel("Option price")
    plt.title(f"Monte Carlo Convergence: {option_type.capitalize()} Option")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    option_type = "call"

    mc_call = mc_price(S, K, T, r, sigma, option_type, n_paths=100000, seed=42)
    bs_call = black_scholes(S, K, T, r, sigma, option_type)
    se_call = mc_standard_error(S, K, T, r, sigma, option_type, n_paths=100000, seed=42)

    print(f"Monte Carlo {option_type} price: {mc_call:.4f}")
    print(f"Black-Scholes {option_type} price: {bs_call:.4f}")
    print(f"Difference: {mc_call - bs_call:.4f}")
    print(f"Standard error: {se_call:.4f}")

    path_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
    plot_convergence(S, K, T, r, sigma, option_type, path_counts, seed=42)