from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Page(object):

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(0)
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        return self

    def goto_home(self):
        self.driver.find_element(By.CLASS_NAME, 'fa-home').click()
        self.wait.until(EC.title_is('Online Store | My Store'))
