import methods

driver = methods.startup()

while True:
    quit = input("quit (y/n)?: ")
    if quit == "y":
        break
    methods.run_hedge(driver)
    print("finished hedging")

driver.quit()