import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes(S, K, r, v, t, T):
    d1 = 1/(v * np.sqrt(T)) * (math.log(S / K) + (r + v**2 / 2) * (T - t))
    d2 = d1 - v * math.sqrt(T - t)

    return norm.cdf(d1) * S - norm.cdf(d2) * K * math.exp(-r * (T - t))

def find_expected_values(S, K, r, v):
# Calculate expected value for a range of time to expiration
    time_to_expiration_range = np.linspace(0, 1, num=100)
    expected_values = []
    for t in time_to_expiration_range:
        # underlying price value should fluctuate: call price purely a function of S and t
        expected_value = black_scholes(S, K, r, v, t, 1)
        expected_values.append(expected_value)
    return np.array(expected_values)

def plot_expected_value(time_to_expiration_range, expected_values):
    # Plot expected value as a function of time to expiration
    plt.plot(time_to_expiration_range, expected_values)
    plt.xlabel('Time To Expiration')
    plt.ylabel('Call Price')
    plt.show()

eval = find_expected_values(100, 100, 0.05, 0.17)
plot_expected_value(np.flip(np.linspace(1, 0, num=100)), eval)