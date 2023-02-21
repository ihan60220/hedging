import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def login_to_bovada(username: str,  password: str, driver: webdriver):
    input("Enter When Web Driver Loaded:")
    fill_out = driver.find_element(By.XPATH, '//*[@id="email"]')
    fill_out.send_keys(username)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    fill_out.send_keys(password)
    fill_out = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
    fill_out.click()


def determine_payout(odds: int, stake: float):
    if odds > 0:
        return odds * (stake / 100)
    elif odds < 0:
        return (100 / -odds) * stake


def isDuplicate(odds: int, oddslist: list[int]):
    if len(oddslist) < 2:
        oddslist.append(odds)
    elif odds != oddslist[-1]:
        oddslist.pop(0)
        oddslist.append(odds)
        return False
    return True


def derivativefinder(oddslist: list):
    dy_dx = oddslist[-1] - oddslist[-2]

    if dy_dx > 0:
        return True
    elif dy_dx < 0:
        return False


def American_to_Decimal(odds: int):
    if odds > 0:
        return odds / 100
    elif odds < 0:
        return 100 / -odds


def determine_StakeB(oddsA: int, stakeA: float, oddsB: int):
    return stakeA * (American_to_Decimal(oddsA) + 1) / (American_to_Decimal(oddsB) + 1)


def makeABet(stakeB: int, driver: webdriver):
    make_bet = driver.find_element(By.XPATH, '//*[@id="default-input--risk"]')
    make_bet.send_keys(str(stakeB))
    make_bet = driver.find_element(By.XPATH, '/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/section/div/div/sp-betslip-area/article/sp-betslip/div/div[2]/footer/button')
    make_bet.click()


def startup():
    # gets rid of some annoying console logs
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # load bovada
    driver.get("https://www.bovada.lv/?overlay=login")
    login_to_bovada("dar58965@gmail.com", "Lpgg3586Rnbx5455", driver)

    # user should get everything set up before proceeding
    input("Press Enter When Done With Setup: ")

    return driver


def run_hedge(driver: webdriver):

    nameA = input("Enter team A name: ")#Can be replaced with a Selenium path later
    oddsA = int(input("Enter odds for A: "))#Can be replaced with a Selenium path later
    stakeA = round(float(input("Enter stakeA: ")), 2)  #Can either be prompted input or detected from Selenium driver
    stakeB = 0
    oddsB_list = []

    # show the range of odds that will make hedging successful
    print("oddsB will need to be greater than:", -oddsA)

    while True:
        # loop every 4 seconds
        time.sleep(4)
        
        # fetch the bet slip
        bet_slip = driver.find_element(By.CLASS_NAME, "top-line")
        teamB = bet_slip.find_elements(By.TAG_NAME, "span")
        nameB = teamB[0].text
        oddsB = int(teamB[1].text)

        print(oddsB)

        # if no change in odds, skip the code below
        if isDuplicate(oddsB, oddsB_list):
            print("No change.")
            continue

        stakeB = determine_StakeB(oddsA, stakeA, oddsB)
        print(stakeB)
        PayoutB = determine_payout(oddsB, stakeB)

        hedge_amount = PayoutB - stakeA

        if hedge_amount < 0:
            print("negative hedge amount:", hedge_amount)
            continue


        if derivativefinder(oddsB_list):
            makeABet(stakeB, driver)
            hedgelog = open("closedpositionslog.txt","a")
            currTime = datetime.now()
            hedgelog.write(nameA + " vs. " + nameB + currTime.strftime("%c") + 
                        "   Total Leveraged: " + str(stakeA + stakeB) + 
                        "   Payout:"+ str(PayoutB - stakeA) + "\n")
            hedgelog.close()
            break