# delta hedging applied to sports betting

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

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


# gets rid of some annoying console logs
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")

# user should get everything set up before proceeding
input("Press Enter When Done With Setup: ")

stakeA = 1.50   #Can either be prompted input or detected from Selenium driver#
stakeB = 0
payoutA = 0
TruepayoutB = 0
oddsBlist = []
timelist = []
dx = []
dydx = 0

for t in range(5):
    # loop every ten seconds
    time.sleep(10)
    
    # fetch the bet slip
    bet_slip = driver.find_elements(By.CLASS_NAME, "top-line")
    teamA = bet_slip[0].find_elements(By.TAG_NAME, "span")
    teamB = bet_slip[1].find_elements(By.TAG_NAME, "span")
    nameA = teamA[0].text
    nameB = teamB[0].text
    oddsA = int(teamA[1].text)
    oddsB = int(teamB[1].text)

    # print the data from bet slip
    print(datetime.now(), nameA, oddsA, nameB, oddsB)

    if isDuplicate() == True:
        continue

    determine_sidepayout(oddsA, stakeA) #Upon locked in stakeA
    stakeB = determinestakeB(oddsA, stakeA, oddsB)
    TruePayoutB = determine_sidepayout(oddsB, stakeB)

    if TruePayoutB - stakeB - stakeA > 0 and derivativefinder(oddsB, oddsBlist):
        # commitSideBbet(stakeB)
        hedgelog = open("closedpositionslog.txt")
        x = datetime.datetime.now()
        hedgelog.write(nameA + " vs. " + nameB + x.strftime("%c") + "   Total Leveraged: " + str(stakeA + stakeB) + "   Payout:"+ str(TruepayoutB - stakeB - stakeA))
        hedgelog.close()
        del oddsBlist[:]

driver.quit()

"""
    make_bets = driver.find_elements(By.ID, "default-input--risk")
    bet_on_A = make_bets[0].send_keys("0.5")
    bet_on_B = make_bets[1].send_keys("0.5")
    place_bets = driver.find_element(By.CLASS_NAME, "betslip-btn-container")
    place_bets = place_bets.find_element(By.TAG_NAME, "button")
    place_bets.click()
"""

#commit Side Bet tries
continue_betting_btn = driver.find_element(By.CLASS_NAME, "continue-betting custom-cta primary cta-large")
continue_betting_btn.click()