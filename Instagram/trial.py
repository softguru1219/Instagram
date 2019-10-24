import json
import os
import time
import csv
import json
import pandas as pd
import pdb

from os import path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver import ActionChains
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.proxy import Proxy, ProxyType
import selenium.webdriver.support.expected_conditions as EC

from accounts import Accounts
from upload_data import instagram
from generateaccountinformation import new_account
from profile_update import update_instagram

DRIVER = 'CHROME'

def smartproxy():
    prox = Proxy()

    prox.proxy_type = ProxyType.MANUAL

    prox.http_proxy = '{hostname}:{port}'.format(hostname = "ca.smartproxy.com", port = 20000)
    prox.ssl_proxy = '{hostname}:{port}'.format(hostname = "ca.smartproxy.com", port = 20000)

    if DRIVER == 'FIREFOX':
        capabilities = webdriver.DesiredCapabilities.FIREFOX
    elif DRIVER == 'CHROME':
        capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    return capabilities

def send_delayed_keys(element, text, delay=0.3) :
    for c in text :
        endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(endtime - time.time())

class create_accounts(object):
    def __init__(self):
        self.success_accounts = []

    def run_selenium(self):
        for i in range(1, 11):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"')
            # chrome_options.add_argument(
            #     '--user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"')
            # driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=smartproxy())
            driver = webdriver.Chrome(chrome_options=chrome_options)

            url = 'https://www.instagram.com/'

            print('Opening Browser')
            driver.get(url)

            # Either get from custom account_maker, or from the random account generator
            # acc = accounts.get_account(idx=3)
            acc = new_account()
            print(acc)

            # wait for page to load up
            locator = 'emailOrPhone'
            try:
                ui.WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
            except TimeoutException:
                print("Not got!")

            time.sleep(3)
            # Enter EMAIL
            action_chains = ActionChains(driver)
            email_field = driver.find_element_by_name('emailOrPhone')
            print(email_field)
            action_chains.move_to_element(email_field)
            send_delayed_keys(email_field, acc['email'], 0.3)
            time.sleep(3)

            # Enter FULLNAME
            fullname_field = driver.find_element_by_name('fullName')
            print(fullname_field)
            action_chains.move_to_element(fullname_field)
            send_delayed_keys(fullname_field, acc['name'], 0.3)
            time.sleep(2)

            # Enter USERNAME
            username_field = driver.find_element_by_name('username')
            print(username_field)
            action_chains.move_to_element(username_field)
            send_delayed_keys(username_field, acc['username'], 0.3)
            time.sleep(2)

            # Enter PASSWORD
            password_field = driver.find_element_by_name('password')
            print(password_field)
            action_chains.move_to_element(password_field)
            send_delayed_keys(password_field, acc['password'], 0.3)
            time.sleep(2)

            # Click on SIGN UP
            sign_up_btn = driver.find_element_by_xpath("//button[@type='submit']")
            sign_up_btn.click()

            time.sleep(5)

            # Select the NOT NOW option for Turn On Notifications
            locator = "//button[contains(@class, 'aOOlW')]"
            try:
                ui.WebDriverWait(driver, 10).until_not(EC.element_to_be_clickable((By.XPATH, locator)))
            except TimeoutException:
                print("Not got!")

            time.sleep(5)

            try:
                age_radio = driver.find_element_by_xpath('//*[@id="igCoreRadioButtonageRadioabove_18"]')
                if age_radio:
                    age_radio.click()
                    time.sleep(2)
                    age_btn = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/button')
                    age_btn.click()
                time.sleep(5)
            except:
                pass

            time.sleep(5)
            not_now = driver.find_elements_by_xpath("//button[contains(@class, 'HoLwm')]")
            if not_now:
                self.success_accounts.append(acc)
                try:
                    not_now[0].click()
                except Exception as e:
                    print(e)
            else:
                break
            driver.close()
            time.sleep(20)

        # Save the created accounts successfully
        if self.success_accounts:
            if path.exists('success_accounts2.json'):
                with open('success_accounts2.json') as f:
                    exist_accounts = json.load(f)
                self.success_accounts = exist_accounts + self.success_accounts

            with open('success_accounts2.json', 'w', encoding='utf8') as f:
                json.dump(self.success_accounts, f, ensure_ascii=False, indent=4)

            # upload the profile
            self.upload_profile()

    def upload_profile(self):
        self.json_to_csv('success_accounts2.json')
        # u = update_instagram()
        # u.update_profile()

    def json_to_csv(self, json_file):
        df = pd.read_json(json_file)
        if path.exists('result10_.csv'):
            os.remove('result10_.csv')
        df.to_csv('result10_.csv')

def main(event, context):
    acc = create_accounts()
    acc.run_selenium()

if __name__ == "__main__":
    main(0, 0)
