"""
Delta Hedging Applied to Sports Bets
"""

import time
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def login_to_bovada(username, password):
    """
    Login to bovada using username and password via Selenium\n
    Need to delay execution until web elements loaded
    """
    input("Enter When Web Driver Loaded:")
    fill_out = driver.find_element(By.XPATH, '//*[@id="email"]')
    fill_out.send_keys(username)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    fill_out.send_keys(password)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
    fill_out.click()


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


def makeABet(stakeB: int):
    """
    If decided that position should be hedged, carry out the position
    """
    make_bet = driver.find_element(By.XPATH, '//*[@id="default-input--risk"]')
    make_bet.send_keys(str(stakeB))
    make_bet = driver.find_element(By.XPATH, '/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/footer/button')
    make_bet.click()


def calculate_volatility(asset_price: list[float]):
    """
    Calculate volatility of the price
    """
    returns = np.roll(asset_price, -1) / asset_price
    returns = returns[:-1] 
    log_returns = np.log(returns)

    return log_returns.std() * np.sqrt(len(asset_price))


def black_scholes(S: float, K: float, r: float, v: float, t:float, T:float):
    """
    Calculates the optimal call price using the Black-Scholes
    formula given the necessary parameters
    """
    d1 = 1/(v * np.sqrt(T)) * (math.log(S / K) + (r + v**2 / 2) * (T - t))
    d2 = d1 - v * math.sqrt(T - t)

    return norm.cdf(d1) * S - norm.cdf(d2) * K * math.exp(-r * (T - t))


"""
Start of Program
"""


# gets rid of some annoying console logs
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")
login_to_bovada("dar58965@gmail.com", "Lpgg3586Rnbx5455")

# user should get everything set up before proceeding
input("Press Enter When Done With Setup: ")

# global variables
nameA = input("Enter team A name: ")#Can be replaced with a Selenium path later
oddsA = int(input("Enter odds for A: "))#Can be replaced with a Selenium path later
stakeA = round(float(input("Enter stakeA: ")), 2)  #Can either be prompted input or detected from Selenium driver
stakeB = 0
oddsB_list = []
PayoutB_list = []

while True:
    # loop every 4 seconds
    time.sleep(4)
    
    # fetch the bet slip
    bet_slip = driver.find_element(By.CLASS_NAME, "top-line")
    teamB = bet_slip.find_elements(By.TAG_NAME, "span")
    nameB = teamB[0].text
    oddsB = int(teamB[1].text)

    print(oddsB)
    PayoutB_list.append(oddsB)

    # if no change in odds, skip the code below
    if isDuplicate(oddsB, oddsB_list):
        print("No change.")
        continue

    stakeB = determine_StakeB(oddsA, stakeA, oddsB)
    print(stakeB)

    # quits if stakeB unreasonably big
    if stakeB > 5:
        continue

    # t = find time elapsed via selenium
    volatility = calculate_volatility(PayoutB_list)
    PayoutB = determine_payout(oddsB, stakeB)
    optimal_price = black_scholes(PayoutB, PayoutB, 0.05, volatility, 0, 1)

    # if stakeB is less than the optimal price, do not execute the hedge
    if stakeB < optimal_price:
        continue


    if PayoutB - stakeA > 0 and derivativefinder(oddsB_list):
        makeABet(stakeB)
        hedgelog = open("closedpositionslog.txt","a")
        currTime = datetime.now()
        hedgelog.write(nameA + " vs. " + nameB + currTime.strftime("%c") + 
                       "   Total Leveraged: " + str(stakeA + stakeB) + 
                       "   Payout:"+ str(PayoutB - stakeB - stakeA) + "\n")
        hedgelog.close()
        del oddsB_list[:]
        break
    else:
        print(str(PayoutB - stakeB - stakeA))


time.sleep(60)

driver.quit()



"""
End of program
"""