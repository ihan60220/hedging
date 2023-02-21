# fetching odds from bovada

import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.bovada.lv/?overlay=login")

# get the name of team
Home = input("Enter name of team: ")

# create a list to contain all odds
container = []

indicator = 0

try:
    while True:
        time.sleep(5)

        try:
            # get all names of the teams, the list could change with website
            names = driver.find_elements(By.CLASS_NAME, "name")
            indexA = 0

            # check if the user's name is in the name list
            for index, name in enumerate(names):
                if name.text == Home:
                    indexA = index
                    break
                if index == len(names) - 1:
                    print("Not a Valid Team Name.")
                    indicator = 1

            # if not a valid name, then exit the program
            if indicator:
                break

            # store the names of the teams
            nameA = names[indexA].text
            nameB = names[indexA + 1].text

            # find the corresponding odds for the teams
            odds = driver.find_elements(By.CLASS_NAME, "bet-price")

            # take care of case when odds are displayed as even
            oddsA = int(odds[3 * indexA + 2].text)
            oddsB = int(odds[3 * indexA + 3].text)

            """
            Delta Hedging Algorithm Here

            """

            # output the odds with timestamps
            container.append((datetime.datetime.now(), oddsA, oddsB))
            print(container[-1][0], nameA, container[-1][1], nameB, container[-1][2])

            # make bets if meets condition
            try:
                buttons = driver.find_elements(By.CLASS_NAME, "bet-btn")
                buttons[3 * indexA + 2].click()
            except:
                print("Bet Not Available.")
            
            # wait for bet slip to load
            time.sleep(5)

            try:
                risk = driver.find_element(By.ID, "default-input--risk")
                risk.send_keys("10")
            except:
                print("trying to click on input box")
        


        except:
            #if something goes wrong while fetching, output error message
            print("Could Not Fetch Odds.")

except KeyboardInterrupt:
    # CTRL-C to exit the program

    print("Program Terminated.")

driver.quit()