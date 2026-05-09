import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from black_scholes import validate_black_scholes_inputs, black_scholes

class PPN:

    def __init__(self, face_value, r, T, principal, S, K, sigma, option_type='call'):
        self.face_value = face_value
        self.r = r
        self.T = T
        self.principal = principal
        self.S = S
        self.K = K
        self.sigma = sigma
        self.option_type = option_type.lower()

        validate_black_scholes_inputs(self.S, self.K, self.T, self.sigma, self.option_type)

    @property
    def zcb_value(self): 

        return self.face_value * np.exp(-self.r * self.T)
    
    @property
    def option_budget(self):

        return self.principal - self.zcb_value
    
    @property
    def option_price(self):
        return black_scholes(self.S, self.K, self.T, self.r, self.sigma, self.option_type)
    
    @property
    def participation_rate(self):
        return self.option_budget / self.option_price
    
    def payoff(self, S_T):
        return self.principal + self.participation_rate * max(S_T - self.S, 0)
    

def rate_sensitivity_analysis():
    rates = [0.01, 0.02, 0.03, 0.04, 0.05]
    participation_rates = []

    for rate in rates:
        ppn = PPN(
            face_value=100,
            r=rate,
            T=3,
            principal=100,
            S=100,
            K=100,
            sigma=0.20
        )

        participation_rates.append(ppn.participation_rate * 100)

    plt.figure()
    plt.plot(rates, participation_rates, marker="o")
    plt.xlabel("Interest Rate")
    plt.ylabel("Participation Rate (%)")
    plt.title("PPN Participation Rate vs Interest Rate")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))
    plt.grid(True)
#   plt.show()

def volatility_sensitivity_analysis():
    vols = [0.1, 0.15, 0.2, 0.25, 0.3]
    participation_rates = []

    for vol in vols:
        ppn = PPN(
            face_value=100,
            r=0.05,
            T=3,
            principal=100,
            S=100,
            K=100,
            sigma=vol
        )

        participation_rates.append(ppn.participation_rate * 100)

    plt.figure()
    plt.plot(vols, participation_rates, marker="o")
    plt.xlabel("Volatility")
    plt.ylabel("Participation Rate (%)")
    plt.title("PPN Participation Rate vs Volatility")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))
    plt.grid(True)  
#   plt.show()

if __name__ == "__main__":
    ppn = PPN(face_value=100, r=0.05, T=3, principal=100, S=100, K=100, sigma=0.2)

    print(f"ZCB value: {ppn.zcb_value:.2f}")
    print(f"Option budget: {ppn.option_budget:.2f}")
    print(f"Option price: {ppn.option_price:.2f}")
    print(f"Participation rate: {ppn.participation_rate:.2%}")
    print(f"Payoff if S_T = 120: {ppn.payoff(120):.2f}")
    rate_sensitivity_analysis()
    volatility_sensitivity_analysis()
    plt.show()
