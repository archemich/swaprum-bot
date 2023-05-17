import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .types import TwitterAccount
from .outlook import Outlook


class Twitter():
    def __init__(self, credentials: TwitterAccount, driver: webdriver.Chrome):
        self.credentials = credentials
        self.driver = driver
        self._username = None

        self.wait = WebDriverWait(driver, 5)
        self.driver.switch_to.new_window('tab')
        self.window = driver.current_window_handle

        driver.get('https://twitter.com')

    def login(self):
        driver = self.driver
        driver.switch_to.window(self.window)
        driver.get('https://twitter.com/login')

        # Send login
        log_input = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
        ActionChains(driver)\
            .send_keys_to_element(log_input, self.credentials['login'])\
            .send_keys(Keys.ENTER)\
            .perform()

        # Send password
        inputs = self.wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'input')))
        pass_input = [i for i in inputs if i.get_attribute('name') == 'password'][0]
        ActionChains(driver)\
            .send_keys_to_element(pass_input, self.credentials['password'])\
            .send_keys(Keys.ENTER)\
            .perform()

        # Here maybe waiting for the password
        is_home = True
        try:
            self.wait.until(lambda d: d.current_url == 'https://twitter.com/home')
        except TimeoutException:
            is_home = False

        if not is_home:
            try:
             el = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="https://help.twitter.com/managing-your-account/additional-information-request-at-login"]')))
            except TimeoutException:
                raise RuntimeError("Unexpected Twitter behaviour")

            try:
                locator = (By.CSS_SELECTOR, 'input[inputmode="email"')
                email_input = self.wait.until(EC.visibility_of_element_located(locator))
                ActionChains(driver) \
                    .send_keys_to_element(email_input, self.credentials['email']['login']) \
                    .send_keys(Keys.ENTER) \
                    .perform()
            except TimeoutException:
                # email doesn't required
                pass

            outlook = Outlook(driver, self.credentials['email'])
            outlook.login()
            verif_code = outlook.find_twitter_verification_code()

            locator = (By.CSS_SELECTOR, 'input[name="text"]')
            verif_input = self.wait.until(EC.visibility_of_element_located(locator))
            ActionChains(driver) \
                .send_keys_to_element(verif_input, verif_code) \
                .send_keys(Keys.ENTER) \
                .perform()

        username = self.username


    def do_swaprum_task(self):
        self.driver.get('https://twitter.com/Swaprum')
        locator = (By.CSS_SELECTOR, 'div[aria-label="Follow @Swaprum"')
        follow = self.wait.until(EC.visibility_of_element_located(locator))
        follow.click()

    def run(self):
        driver = self.driver
        self.login()
        self.do_swaprum_task()

    @property
    def username(self):
        if self._username:
            return self._username
        prev_handler = self.driver.current_window_handle
        self.driver.switch_to.new_window('tab')
        self.cur_handler = self.driver.current_window_handle
        if self.driver.current_url != 'https://twitter.com/home':
            self.driver.get('https://twitter.com/home')
        profile_link = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Profile"]')))
        self._username = '@' + re.match('.*/(.*)$', profile_link.get_attribute('href')).group(1)

        self.driver.close()
        self.driver.switch_to.window(prev_handler)
        return self._username
