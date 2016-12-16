from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.page import Page


class PageWCart(Page):

    def get_quantity(self):
        return int(self.driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text)

    def goto_checkout_page(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Checkout').click()
        self.wait.until(EC.title_is('Checkout | My Store'))
