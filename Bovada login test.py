#Fill out login information Selenium path
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get("https://www.bovada.lv/?overlay=login")

time.sleep(5)
fill_out = driver.find_element(By.XPATH, '//*[@id="email"]')
fill_out.send_keys("dar58965@gmail.com")
time.sleep(1.5)
fill_out = driver.find_element(By.XPATH, '//*[@id="login-password"]')
fill_out.send_keys("Lpgg3586Rnbx5455")
time.sleep(1.5)
fill_out = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
fill_out.click()
