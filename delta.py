# delta hedging applied to sports betting
import os
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

# gets rid of some annoying console logs
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")

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
    if stakeB > 5:
        break

    TruePayoutB = determine_sidepayout(oddsB, stakeB)

    if TruePayoutB - stakeB - stakeA > 0 and derivativefinder(oddsBlist):
        makeABet(stakeB)
        hedgelog = open("closedpositionslog.txt","a")
        currTime = datetime.now()
        hedgelog.write(nameA + " vs. " + nameB + currTime.strftime("%c") + "   Total Leveraged: " + str(stakeA + stakeB) + "   Payout:"+ str(TruePayoutB - stakeB - stakeA))
        hedgelog.close()
        del oddsBlist[:]
        break
    else:
        print(str(TruePayoutB - stakeB - stakeA))


time.sleep(60)

driver.quit()

#end of program