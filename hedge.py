# fetching odds from bovada

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.bovada.lv/sports/basketball")

while True:
    time.sleep(5)

    try:
        elements = driver.find_elements(By.CLASS_NAME, "bet-price")
        oddsA = int(elements[2].text)
        oddsB = int(elements[3].text)
        print(oddsA, oddsB)
    except:
        pass

driver.quit()