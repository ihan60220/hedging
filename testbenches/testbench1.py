from datetime import datetime

#unit testing

#Determines value given out if a side wins (This one worked)
def determine_sidepayout(odds, stake):
    if odds > 0:
        return odds * (stake / 100) + stake
    elif odds < 0:
        return (100 / -odds) * stake + stake

def isDuplicate(odds, oddslist):
    if oddslist == []:
        oddslist.append(odds)
    elif odds != oddslist[-1]:
        return False
    return True

#Basic derivative algorithm. Will get better over time with better analysis and data feeding. Look into databases
def derivativefinder(oddslist):
    dydx = oddslist[-1] - oddslist[-2]
    if dydx > 0:
        return True
    elif dydx < 0:
        return False
    if len(oddslist) > 1:
        oddslist.pop(0)

def American_to_Decimal(odds):
    if odds > 0:
        return odds / 100
    elif odds < 0:
        return 100 / -odds

def determinestakeB(oddsA, stakeA, oddsB):
    return stakeA * (American_to_Decimal(oddsA) + 1) / (American_to_Decimal(oddsB) + 1)
    

oddsA = -150
stakeA = 10
oddsB = -120
print(determinestakeB(oddsA, stakeA, oddsB))

"""
lamestakeB = (fullstakeB / 2) - (stake / 2) + stake
    stakeB =  (fullstakeB + lamestakeB) / 2
"""