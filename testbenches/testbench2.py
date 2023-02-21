import math
import numpy as np
import pandas as pd
from scipy.stats import norm

def determine_risk_free_rate(odds):
    if odds > 0:
        return 100 / (100 + odds)
    elif odds < 0:
        return -odds/(-odds + 100)
    
def calculate_volatility(asset_price):
    log_returns = np.log(asset_price / np.roll(asset_price, 1))
    volatility = log_returns.std() * np.sqrt(len(asset_price))
    return volatility
    
def calculate_confidence(volatility, confidence_level, asset_price):
    # Calculate standard error
    standard_error = volatility / np.sqrt(len(asset_price))
    
    # Calculate confidence interval
    z_score = norm.ppf((1 + confidence_level) / 2)
    lower_bound = volatility - z_score * standard_error
    upper_bound = volatility + z_score * standard_error
    
    return lower_bound, upper_bound, z_score

def determine_steps(z_score):
    return math.ceil(z_score**2)

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

def use_binomial_tree_to_find_ideal_time(odds, strike, risk_free_rate, volatility, steps):
# Calculate expected value for a range of time to expiration
    time_to_expiration_range = np.linspace(0, 1, num=100)
    expected_values = []
    for t in time_to_expiration_range:
        expected_value = binomial_tree_model(odds, strike, risk_free_rate, volatility, t, steps)
        expected_values.append(expected_value)
        

odds = 100
asset_price = [100, 200, 300, 400, 500]
volatility = calculate_volatility(asset_price)
confidence = calculate_confidence(volatility, 0.95, asset_price)
steps = determine_steps(confidence[2])
strike = 1
risk_free_rate = 1
time_to_expiration = 1
option_value = binomial_tree_model(odds, strike, risk_free_rate, volatility, time_to_expiration, steps)
print(option_value)

