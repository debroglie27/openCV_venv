from selenium import webdriver
import time
import os
from pathlib import Path
from dotenv import load_dotenv
import json

env_path = Path('../.env')
load_dotenv(dotenv_path=env_path)

EMAIL_ID = os.environ.get('MS_TEAMS_EMAIL')
EMAIL_PASS = os.environ.get('MS_TEAMS_PASSWORD')

# Loading The Time Table
with open('./time_table.json') as f:
    time_table = json.load(f)

# Web Driver for Firefox
driver = webdriver.Firefox()

while True:
    driver.get("https://login.microsoftonline.com/common/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=0170a2b5-88be-4501-b346-7e5509ae5646&&client-request-id=081c4710-8d26-4e00-bf2f-e65bfebff857&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=1eaec18b-2f7c-410a-8bf5-cffbd608cce6&domain_hint=")

    # All the xpath of Teams
    cg_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/ng-include/div"
    minor_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div/ng-include/div"
    rtsd_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[4]/div/ng-include/div"
    ds_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[5]/div/ng-include/div"
    se_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[3]/div[2]/div/ng-include/div"
    cn_xpath = "/html/body/div[1]/div[2]/div[2]/div[1]/teams-grid/div/div[2]/div[1]/div[1]/div/div[1]/div[3]/div[3]/div/ng-include/div"

    # List of Team xpaths
    team_xpaths = [cg_xpath, minor_xpath, rtsd_xpath, ds_xpath, se_xpath, cn_xpath]
    team_names = ["CG", "Minor", "RTSD", "DS", "SE", "CN"]

    # If SignIn page accessed through MS Teams main page
    # sign_in_button = driver.find_element_by_class_name("c-button.f-secondary.xs-ow-mt-10.m-ow-mt-30.ow-bvr-signin")
    # sign_in_button.click()
    # time.sleep(5)
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(1)

    # Providing Email_id as Input
    email_entry = driver.find_element_by_id("i0116")
    email_entry.send_keys(EMAIL_ID)
    next_button = driver.find_element_by_id("idSIButton9")
    next_button.click()
    time.sleep(2)

    counter = 10
    while True:
        try:
            # Providing the Password
            password_entry = driver.find_element_by_id("i0118")
            password_entry.send_keys(EMAIL_PASS)
            sign_in_button = driver.find_element_by_id("idSIButton9")
            sign_in_button.click()
            time.sleep(2)
            break
        except Exception:
            if counter > 0:
                time.sleep(2)
                counter -= 1
            else:
                driver.quit()

    counter = 10
    while True:
        try:
            # Clicking the NO Button so that we don't remain signed in
            no_button = driver.find_element_by_id("idBtn_Back")
            no_button.click()
            time.sleep(60)
            break
        except Exception:
            if counter > 0:
                time.sleep(2)
                counter -= 1
            else:
                driver.quit()

    counter = 10
    while True:
        try:
            dismiss_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/button[2]")
            dismiss_button.click()
            team_cards = {}

            for i in range(6):
                team_card = driver.find_elements_by_xpath(team_xpaths[i])
                team_cards[team_names[i]] = team_card
            break
        except Exception:
            if counter > 0:
                time.sleep(10)
                counter -= 1
            else:
                driver.quit()

    weekday = time.strftime("%A", time.localtime())

    if weekday == "Saturday" or weekday == "Sunday":
        driver.quit()
        time.sleep(86400)
        continue

    driver.quit()
    time.sleep(63000)

# sign_in_button.send_keys(Keys.RETURN)

# driver.quit()
