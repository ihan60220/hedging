import math
import numpy as np
from scipy.stats import norm

# feeding data points manually to observe behavior

def determine_payout(odds: int, stake: float):
    """
    Determines the return on a single position if a side wins\n
    """
    if odds > 0:
        return odds * (stake / 100)
    elif odds < 0:
        return (100 / -odds) * stake


def isDuplicate(odds: int, oddslist: list[int]):
    """
    Returns true if the odds have not changed\n
    Returns false if the odds have changed from previous value
    """
    if len(oddslist) < 2:
        oddslist.append(odds)
        print("Less than two data points.")
        return False
    elif odds != oddslist[-1]:
        oddslist.pop(0)
        oddslist.append(odds)
        return False
    return True


def derivativefinder(oddslist: list):
    """
    Takes the rate of change of the odds\n
    Returns true if the derivative is positive\n
    Returns false if the derivative is negative
    """
    dy_dx = oddslist[-1] - oddslist[-2]

    if dy_dx > 0:
        return True
    elif dy_dx < 0:
        return False


def American_to_Decimal(odds: int):
    """
    Turns american odds into decimal odds
    """
    if odds > 0:
        return odds / 100
    elif odds < 0:
        return 100 / -odds


def determine_StakeB(oddsA: int, stakeA: float, oddsB: int):
    """
    Calculate what StakeB must be in order to hedge position\n
    May result in a negative return, in which case should not hedge
    """
    return stakeA * (American_to_Decimal(oddsA) + 1) / (American_to_Decimal(oddsB) + 1)


def calculate_volatility(asset_price: list[float]):
    """
    Calculate volatility of the price
    """
    if len(asset_price) < 2:
        print("too few data points.")
        return 0
    
    returns = np.roll(asset_price, -1) / asset_price
    returns = returns[:-1] 
    log_returns = np.log(returns)

    return log_returns.std() * np.sqrt(len(asset_price))


def black_scholes(S: float, K: float, r: float, v: float, t:float, T:float):
    """
    Calculates the optimal call price using the Black-Scholes
    formula given the necessary parameters
    """
    if v == 0:
        # in the case where price is constant, the option value has no ext value

        return S - K * math.exp(-r * (T - t))
    else :
        d1 = 1/(v * np.sqrt(T)) * (math.log(S / K) + (r + v**2 / 2) * (T - t))
        d2 = d1 - v * math.sqrt(T - t)

    return norm.cdf(d1) * S - norm.cdf(d2) * K * math.exp(-r * (T - t))


nameA = "Team A"
oddsA = int(input("Enter odds for A: "))
stakeA = round(float(input("Enter stakeA: ")), 2)
stakeB = 0
oddsB_list = []
PayoutB_list = []


while True:
    nameB = "Team B"
    oddsB = float(input("Enter the oddsB: "))

    print(oddsB)
    PayoutB_list.append(American_to_Decimal(oddsB))
    print(PayoutB_list)

    # if no change in odds, skip the code below
    if isDuplicate(oddsB, oddsB_list):
        print("No change in oddsB.")
        continue

    stakeB = determine_StakeB(oddsA, stakeA, oddsB)
    print("stakeB: ", stakeB)

    # t = find time elapsed via selenium
    volatility = calculate_volatility(PayoutB_list)
    print("volatility: ", volatility)
    PayoutB = determine_payout(oddsB, stakeB)
    print("payout:", PayoutB)
    optimal_price = black_scholes(PayoutB, PayoutB, 0.05, volatility, 0, 1/365)
    print("optimal price:", optimal_price)

    # if stakeB is less than the optimal price, do not execute the hedge
    if stakeB > optimal_price:
        continue

    if PayoutB - stakeA > 0 and derivativefinder(oddsB_list):
        print("bet executed, net return =", PayoutB - stakeA)
    else:
        print("not executed, net return =", PayoutB - stakeA)
