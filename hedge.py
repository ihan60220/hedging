# fetching odds from bovada

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

Home = input("Enter name of team: ")

driver = webdriver.Chrome()

driver.get("https://www.bovada.lv/sports/basketball")

while True:
    time.sleep(5)

    try:
        names = driver.find_elements(By.CLASS_NAME, "name")
        indexA = 0
        for index, name in enumerate(names):
            if name.text == Home:
                indexA = index
        nameA = names[indexA].text
        nameB = names[indexA + 1].text
        odds = driver.find_elements(By.CLASS_NAME, "bet-price")
        oddsA = int(odds[3 * indexA + 2].text)
        oddsB = int(odds[3 * indexA + 3].text)
        print(nameA, oddsA, nameB, oddsB)
    except:
        print("could not fetch")

driver.quit()