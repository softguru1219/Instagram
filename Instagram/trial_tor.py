import os
import time
from selenium import webdriver
from generateaccountinformation import new_account
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import webbrowser

def send_delayed_keys(element, text, delay=0.3) :
    for c in text :
        endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(endtime - time.time())


# profile = FirefoxProfile(r'/Users/mehullala/Library/Application Support/TorBrowser-Data/Browser/o78olzo7.default') #change this based on your installation
profile = FirefoxProfile('C:\\Users\\Server\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default') #change this based on your installation
# profile = FirefoxProfile(r'C:\\Users\\Server\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\e9yrw0ql.default')
profile.set_preference('network.proxy.type', 1)
# profile.set_preference("network.proxy.http", "localhost")
# profile.set_preference("network.proxy.http_port", 3128)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9150)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.set_preference("browser.privatebrowsing.autostart", True)
profile.update_preferences()

for i in range(1,10):

    driver = webdriver.Firefox(firefox_profile= profile)

    url = 'https://www.instagram.com/'
    acc = new_account()
    print(acc)

    driver.get(url)
    time.sleep(3)

    # Enter EMAIL
    email_field = driver.find_element_by_name('emailOrPhone')
    print(email_field)
    # email_field.send_keys(acc['email'])
    send_delayed_keys(email_field, acc['email'], 0.3)
    time.sleep(3)

    # Enter USERNAME
    username_field = driver.find_element_by_name('username')
    print(username_field)
    send_delayed_keys(username_field, acc['username'], 0.3)
    time.sleep(2)

    # Enter FULLNAME
    fullname_field = driver.find_element_by_name('fullName')
    print(fullname_field)
    send_delayed_keys(fullname_field, acc['name'], 0.3)
    time.sleep(2)

    # Enter PASSWORD
    password_field = driver.find_element_by_name('password')
    print(password_field)
    send_delayed_keys(password_field, acc['password'], 0.3)
    time.sleep(2)

    # Click on SIGN UP
    sign_up_btn = driver.find_element_by_xpath("//button[@type='submit']")
    sign_up_btn.click()

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

    time.sleep(10)
    not_now = driver.find_elements_by_xpath("//button[contains(@class, 'HoLwm')]")
    if not_now:
        not_now[1].click()

    driver.close()
    #time.sleep(20)



