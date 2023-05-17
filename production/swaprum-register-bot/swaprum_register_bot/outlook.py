import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .types import Email
class Outlook():
    def __init__(self, driver: webdriver.Chrome, credentials: Email):
        self.credentials = credentials
        self.driver = driver
        self.logged = False

        self.wait = WebDriverWait(driver, 5)
        self.driver.switch_to.new_window('tab')
        self.window = driver.current_window_handle
        self.driver.get('https://outlook.live.com/mail')

    def login(self):
        driver = self.driver
        self.driver.switch_to.new_window('tab')
        login_window = driver.current_window_handle
        self.driver.get('https://login.live.com/')

        # send login
        locator = (By.CSS_SELECTOR, 'input[name="loginfmt"]')
        login_input = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(driver)\
        .send_keys_to_element(login_input, self.credentials['login'])\
        .send_keys(Keys.ENTER)\
        .perform()

        # send password
        locator = (By.CSS_SELECTOR, 'input[name="passwd"]')
        passwd_input = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(driver)\
        .send_keys_to_element(passwd_input, self.credentials['password'])\
        .send_keys(Keys.ENTER)\
        .perform()

        # do not log out
        try:
            locator = (By.CSS_SELECTOR, 'input[type="submit"]')
            yes_but = self.wait.until(EC.visibility_of_element_located(locator))
            ActionChains(driver) \
                .click(yes_but) \
                .perform()
        except NoSuchElementException as e:
            # Form hasn't appeared
            pass

        self.logged = True
        self.driver.close()
        self.driver.switch_to.window(self.window)
        self.driver.refresh()

    def find_twitter_verification_code(self):
        title_text = 'Your Twitter confirmation code is'
        locator = (By.XPATH, f'//span[@title and contains(text(), "{title_text}")]')
        span = self.wait.until(EC.visibility_of_element_located(locator))
        return re.match(f'{title_text} (.*)', span.text).group(1)