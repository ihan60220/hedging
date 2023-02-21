import math
import numpy as np
from scipy.stats import norm

def binomial_tree_model(odds, strike, risk_free_rate, volatility, time_to_expiration, steps):
    # Calculate the up and down factors
    time_step = time_to_expiration / steps
    u = math.exp(volatility * math.sqrt(time_step))
    d = 1 / u

    # Calculate the probability of an up move
    p = (math.exp(risk_free_rate * time_step) - d) / (u - d)

    # Build the binomial tree
    odds_tree = []
    for i in range(steps + 1):
        odds_row = []
        for j in range(i + 1):
            odds_up = odds * u ** (i - j) * d ** j
            odds_row.append(odds_up)
        odds_tree.append(odds_row)

    # Backpropagate through the tree to calculate the value of the option
    value_tree = []
    for i in range(steps + 1):
        value_step = []

        for j in range(steps - i + 1):
            if i == 0:
                # value of option at the expirary date is its intrinsic value (no time value)
                value = max(odds_tree[steps][j] - strike, 0)
            else:
                value_up = value_tree[i - 1][j]
                value_down = value_tree[i - 1][j + 1]
                # take the expected value of the current node
                value = math.exp(-risk_free_rate * time_step) * p * value_up + (1 - p) * value_down
            value_step.append(value)

        value_tree.append(value_step)
        
    # The final value of the option is the value of the option at the last step of the tree
    return value_tree[steps][0]

def black_scholes(S, K, r, v, T):
    d1 = 1/(v * np.sqrt(T)) * (math.log(S / K) + (r + v**2 / 2) * T)
    d2 = d1 - v * math.sqrt(T)

    return norm.cdf(d1) * S - norm.cdf(d2) * K * math.exp(-r * T)


# get the necessary parameters
S = float(input("Spot price: "))
K = float(input("Strike price: "))
r = float(input("Risk free rate: "))
v = float(input("Volatility: "))
T = float(input("Time of expiration: "))

binomial = binomial_tree_model(S, K, r, v, T, 30)
bs = black_scholes(S, K, r, v, T)

# see that both models agree
print("BOPM:", binomial, "BS:", bs)
print("Percent error: ", round(abs(bs - binomial) / binomial * 100), "%\n")
