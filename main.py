# delta hedging applied to sports betting
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def login_to_bovada(username, password):
    input("Enter When Web Driver Loaded:")
    fill_out = driver.find_element(By.XPATH, '//*[@id="email"]')
    fill_out.send_keys(username)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    fill_out.send_keys(password)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
    fill_out.click()

#Determines value given out if a side wins (This one worked) superflous: need only consider net return
def determine_sidepayout(odds, stake):
    if odds > 0:
        return odds * (stake / 100) + stake
    elif odds < 0:
        return (100 / -odds) * stake + stake

def isDuplicate(odds, oddslist):
    if len(oddslist) < 2:
        oddslist.append(odds)
    elif odds != oddslist[-1]:
        oddslist.pop(0)
        oddslist.append(odds)
        return False
    return True

#Basic derivative algorithm. Will get better over time with better analysis and data feeding. Look into databases
def derivativefinder(oddslist):
    dydx = oddslist[-1] - oddslist[-2]
    if dydx > 0:
        return True
    elif dydx < 0:
        return False

def American_to_Decimal(odds):
    if odds > 0:
        return odds / 100
    elif odds < 0:
        return 100 / -odds

def determinestakeB(oddsA, stakeA, oddsB):
    return stakeA * (American_to_Decimal(oddsA) + 1) / (American_to_Decimal(oddsB) + 1)

def makeABet(stakeB):
    make_bet = driver.find_element(By.XPATH, '//*[@id="default-input--risk"]')
    make_bet.send_keys(str(stakeB))
    make_bet = driver.find_element(By.XPATH, '/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/footer/button')
    make_bet.click()

data_points = 0

def determine_risk_free_rate(odds):
    if odds > 0:
        return 100 / (100 + odds)
    elif odds < 0:
        return -odds/(-odds + 100)

#The asset price is determined by the Selenium web driver
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
                print(value_up)
                value_row.append(value_up)
            else:
                odds_down = odds_tree[i][j]
                value_down = odds_down - strike
                value = p * value_up + (1 - p) * value_down
                print(value_down)
                value_row.append(value)
            
        value_tree.append(value_row)
    # calculate the expected value of the return on the bet
    return value_tree[steps][0]
        
    # The final value of the option is the value of the option at the last step of the tree
    return expected_value

def update_binomial_tree_model(new_odds, strike, risk_free_rate, volatility, time_to_expiration, steps):
    data_points = data_points + 1
    return binomial_tree_model(new_odds, strike, risk_free_rate, volatility, time_to_expiration, steps)

def find_expected_values(odds, strike, risk_free_rate, volatility, steps):
# Calculate expected value for a range of time to expiration
    time_to_expiration_range = np.linspace(0, 1, num=100)
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

# Determine if executing hedge bet is positive
def is_hedgebet_positive(hedge_bet_expected_value, best_time):
    if hedge_bet_expected_value > 0:
        print("Executing hedge bet at time", best_time, "is good.")
    else:
        print("Executing hedge bet at time", best_time, "is bad.")

# gets rid of some annoying console logs
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")
login_to_bovada("dar58965@gmail.com", "Lpgg3586Rnbx5455")

# user should get everything set up before proceeding
input("Press Enter When Done With Setup: ")

#global variables for david
nameA = input("Enter team A name: ")#Can be replaced with a Selenium path later
oddsA = int(input("Enter odds for A: "))#Can be replaced with a Selenium path later
stakeA = round(float(input("Enter stakeA: ")), 2)  #Can either be prompted input or detected from Selenium driver
stakeB = 0
oddsBlist = []

while True:
    # loop every 4 seconds
    time.sleep(4)
    
    # fetch the bet slip
    bet_slip = driver.find_element(By.CLASS_NAME, "top-line")
    teamB = bet_slip.find_elements(By.TAG_NAME, "span")
    nameB = teamB[0].text
    oddsB = int(teamB[1].text)

    print(oddsB)

    if isDuplicate(oddsB, oddsBlist) == True:
        continue

    stakeB = determinestakeB(oddsA, stakeA, oddsB)
    print(stakeB)
    # quits if stakeB unreasonably big
    if stakeB > 5:
        continue

    TruePayoutB = determine_sidepayout(oddsB, stakeB)

    if TruePayoutB - stakeB - stakeA > 0 and not derivativefinder(oddsBlist):
        makeABet(stakeB)
        hedgelog = open("closedpositionslog.txt","a")
        currTime = datetime.now()
        hedgelog.write(nameA + " vs. " + nameB + currTime.strftime("%c") + 
                       "   Total Leveraged: " + str(stakeA + stakeB) + 
                       "   Payout:"+ str(TruePayoutB - stakeB - stakeA) + "\n")
        hedgelog.close()
        del oddsBlist[:]
        break
    else:
        print(str(TruePayoutB - stakeB - stakeA))


time.sleep(60)

driver.quit()

#end of program