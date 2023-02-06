import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

data_points = 0
def determine_risk_free_rate(odds):
    risk_free_rate = 100 / (100 + odds)
    risk_free_rate = risk_free_rate / 100
    return(risk_free_rate)

#The asset price is determined by the Selenium web driver
def calculate_volatility(asset_price, data_points):
    log_returns = np.log(asset_price / asset_price.shift(1))
    volatility = log_returns.std() * np.sqrt(data_points)
    return volatility

def calculate_volatility_and_confidence(volatility, confidence_level):
    # Calculate standard error
    standard_error = volatility / np.sqrt(len(asset_price))
    
    # Calculate confidence interval
    z_score = norm.ppf((1 + confidence_level) / 2)
    lower_bound = volatility - z_score * standard_error
    upper_bound = volatility + z_score * standard_error
    
    return volatility, lower_bound, upper_bound, z_score

def determine_steps(z_score):
    return math.ciel(z_score**2)

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
            odds_up = odds * u ** (steps - j) * d ** j
            odds_row.append(odds_up)
        odds_tree.append(odds_row)

    # Backpropagate through the tree to calculate the value of the option
    value_tree = []
    for i in range(steps + 1):
        value_row = []
        for j in range(i + 1):
            odds_up = odds_tree[i][j]
            value_up = odds_up - strike
            if i == steps:
                value_row.append(value_up)
            else:
                odds_down = odds_tree[i][j]
                value_down = odds_down - strike
                value = p * value_up + (1 - p) * value_down
                value_row.append(value)
        value_tree.append(value_row)
    option_value = value_tree[steps][0]
    # The final value of the option is the value of the option at the last step of the tree
    return option_value

def update_binomial_tree_model(new_odds, strike, risk_free_rate, volatility, time_to_expiration, steps):
    data_points = data_points + 1
    return binomial_tree_model(new_odds, strike, risk_free_rate, volatility, time_to_expiration, steps)

def use_binomial_tree_to_find_ideal_time():
# Calculate expected value for a range of time to expiration
time_to_expiration_range = np.linspace(0, 1, num=100)
expected_values = []
for t in time_to_expiration_range:
    expected_value = binomial_tree_model(odds, strike, risk_free_rate, volatility, t, steps)
    expected_values.append(expected_value)

# Plot expected value as a function of time to expiration
plt.plot(time_to_expiration_range, expected_values)
plt.xlabel('Time to expiration')
plt.ylabel('Expected value')
plt.show()

# Determine best time to execute hedge bet
best_time_index = np.argmax(expected_values)
best_time = time_to_expiration_range[best_time_index]

# Calculate expected value of hedge bet
hedge_bet_expected_value = expected_values[best_time_index] - oddsA

# Determine if executing hedge bet is positive
if hedge_bet_expected_value > 0:
    print("Executing hedge bet at time", best_time, "is good.")
else:
    print("Executing hedge bet at time", best_time, "is bad.")


"""
We need to determine the time_of_expiration through a Selenium web scrape of the time remaining element and the quarter element.
We can't use user input every time because this model is executed every time there is a novel data point.
The good thing is we probably only need to fetch it a single time for the calculate_volatility function and the binomial_tree_model function. 
"""
