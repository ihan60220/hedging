import numpy as np

def calculate_volatility(asset_price):
    returns = np.roll(asset_price, -1) / asset_price
    returns = returns[:-1]
    print(returns)   
    log_returns = np.log(returns)
    print(log_returns)
    volatility = log_returns.std() * np.sqrt(len(asset_price))
    return volatility


print(calculate_volatility([100, 200, 300, 400, 500]))