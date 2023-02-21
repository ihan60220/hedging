def determine_payout(odds: int, stake: float):
    if odds > 0:
        return odds * (stake / 100)
    elif odds < 0:
        return (100 / -odds) * stake
    

def determine_hedge_profit(stakeA, oddsB, stakeB):
    payoutB = determine_payout(oddsB, stakeB)
    return payoutB - stakeA


def is_decreasing(oddslist: list):
    if len(oddslist < 2):
        return False
    
    dy_dx = oddslist[-1] - oddslist[-2]

    if dy_dx < 0:
        return True
    else:
        return False
    

def american_to_decimal(odds: int):
    if odds > 0:
        return odds / 100
    elif odds < 0:
        return 100 / -odds
    

def determine_stakeB(oddsA: int, stakeA: float, oddsB: int):
    stakeB = stakeA * (american_to_decimal(oddsA) + 1) / (american_to_decimal(oddsB) + 1)
    return round(stakeB, 2)