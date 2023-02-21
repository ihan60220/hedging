from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


def login_to_bovada(username: str,  password: str, driver: webdriver) -> bool:
    try:
        input("Enter When Web Driver Loaded:")
        fetched = driver.find_element(By.XPATH, '//*[@id="email"]')
        fetched.send_keys(username)
        fetched = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        fetched.send_keys(password)
        fetched = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
        fetched.click()
        return True
    except:
        return False
    

def fetch_teamB_name(driver: webdriver) -> None:
    try:
        return driver.find_element(By.XPATH, "/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/div[2]/div/sp-betslip-single-tab/ul/li/section/sp-bet/div/sp-singlebet/section/div[1]/h5/span")
    except:
        print("teamB name could not be fetched")
        return False
        

def fetch_oddsB(driver: webdriver) -> None:
    try:
        return driver.find_element(By.XPATH, "/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/div[2]/div/sp-betslip-single-tab/ul/li/section/sp-bet/div/sp-singlebet/section/div[1]/span")
    except:
        print("oddsB could not be fetched")
    

def make_a_bet(stake: int, driver: webdriver) -> None:
    make_bet = driver.find_element(By.XPATH, '//*[@id="default-input--risk"]')
    make_bet.send_keys(str(stake))
    make_bet = driver.find_element(By.XPATH, '/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/footer/button')
    make_bet.click()


def produce_log(nameA, nameB, leveraged, hedge_profit):
    try:
        hedge_log = open("closedpositions.txt", "a")
    except:
        print("could not find closedpositions.txt")
    curr_time = datetime.now()
    hedge_log.write(curr_time.strftime("%c"), "\t", nameA, "vs", nameB) 
    hedge_log.write("Total Leveraged:", leveraged, "\t", "Payout:", hedge_profit)
    hedge_log.write("\n")
    hedge_log.close()