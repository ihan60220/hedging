# delta hedging applied to sports betting

import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# gets rid of some annoying console logs
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")

# user should get everything set up before proceeding
input("Press Enter When Done With Setup: ")

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
    print(nameA, oddsA, nameB, oddsB)
    
    """
    Delta Hedging Algorithm Here

    """

    # if determined that bet should be hedged for teamA
    make_bets = driver.find_elements(By.ID, "default-input--risk")
    bet_on_A = make_bets[0].send_keys("1")
    bet_on_B = make_bets[1].send_keys("1")
    place_bets = driver.find_element(By.CLASS_NAME, "betslip-btn-container")
    place_bets = place_bets.find_element(By.TAG_NAME, "button")
    place_bets.click()
    

driver.quit()