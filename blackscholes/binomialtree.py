import math
import numpy as np
import matplotlib.pyplot as plt


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


def find_expected_values(odds, strike, risk_free_rate, volatility, steps):
# Calculate expected value for a range of time to expiration
    time_to_expiration_range = np.linspace(1, 0.05, num=20)
    expected_values = []
    for t in time_to_expiration_range:
        expected_value = binomial_tree_model(odds, strike, risk_free_rate, volatility, t, steps)
        expected_values.append(expected_value)
    return expected_values


def plot_expected_value(time_to_expiration_range, expected_values):
    # Plot expected value as a function of time to expiration
    plt.plot(time_to_expiration_range, expected_values)
    plt.xlabel('Time to expiration')
    plt.ylabel('Expected value')
    plt.show()


def determine_best_time(time_to_expiration_range, expected_values):
    # Determine best time to execute hedge bet
    best_time_index = np.argmax(expected_values)
    return time_to_expiration_range[best_time_index]


def hedgebet_expected_value(expected_values, oddsA):
    # Calculate expected value of hedge bet
    best_time_index = np.argmax(expected_values)
    return expected_values[best_time_index] - oddsA


def is_hedgebet_positive(hedge_bet_expected_value, best_time):
    if hedge_bet_expected_value > 0:
        print("Executing hedge bet at time", best_time, "is good.")
    else:
        print("Executing hedge bet at time", best_time, "is bad.")



price = binomial_tree_model()
