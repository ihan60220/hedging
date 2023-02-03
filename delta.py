# fetching odds from bovada

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

for t in range(10):
    # loop every five seconds
    time.sleep(5)
    
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

driver.quit()