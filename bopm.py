# binomial option pricing model
import math

def binomial_tree_model(odds, strike, volatility, time_to_expiration, steps):
    # Calculate the up and down factors
    time_step = time_to_expiration / steps
    u = math.exp(volatility * math.sqrt(time_step))
    d = 1 / u

    # Calculate the probability of an up move
    p = (1 - d) / (u - d)

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
                value = p * value_up + (1 - p) * value_down
            value_step.append(value)

        value_tree.append(value_step)
        
    # The final value of the option is the value of the option at the last step of the tree
    return value_tree[steps][0]

binomial_tree_model(0.5, 100, )