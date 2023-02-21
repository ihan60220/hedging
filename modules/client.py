import bovada
import hedgemath
import time
from selenium import webdriver

def startup():
    print("hedge betting")

    # gets rid of some annoying console logs
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # load bovada
    driver.get("https://www.bovada.lv/?overlay=login")

    # keep trying to log into bovada until succeeed
    while not bovada.login_to_bovada("dar58965@gmail.com", "Lpgg3586Rnbx5455", driver):
        pass

    return driver

def run_hedge(driver):

    nameA = input("Enter team A name: ")    # Can be replaced with a Selenium path later
    oddsA = int(input("Enter odds for A: "))    # Can be replaced with a Selenium path later
    stakeA = round(float(input("Enter stakeA: ")), 2)   # Can either be prompted input or detected from Selenium driver
    stakeB = 0
    oddsB_list = []

    print("oddsB will have to be higher than:", -oddsA)

    while True:
        time.sleep(3)
        
        nameB = bovada.fetch_teamB_name(driver)
        oddsB = bovada.fetch_oddsB(driver)
        oddsB_list.append(oddsB)
        print("oddsB:", oddsB)

        stakeB = hedgemath.determine_stakeB(oddsA, stakeA, oddsB)
        hedge_profit = hedgemath.determine_hedge_profit(stakeA, oddsB, stakeB)
        leveraged = stakeA + stakeB

        if hedge_profit < 0:
            print("cannot be hedged")
            print("hedge profit: ", hedge_profit)
            continue
        else:
            print("can be hedged")
            stakeB = hedgemath.determine_stakeB(oddsA, stakeA, oddsB)
            print("stakeB:", stakeB)
            payoutB = hedgemath.determine_payout(oddsB, stakeB)
            print("hedge amount: ", hedge_profit)

        if hedgemath.is_decreasing(oddsB_list):
            bovada.make_a_bet(stakeB, driver)
            bovada.produce_log(nameA, nameB, leveraged, hedge_profit)
            break
    
    print("position closed")