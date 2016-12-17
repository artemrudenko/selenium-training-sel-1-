from selenium.common.exceptions import NoSuchElementException

from pages.page import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage(Page):

    url = "http://localhost/litecart/en/checkout"
    # url = "http://192.168.1.5/litecart/en/checkout"

    def open(self):
        if not self.is_on_page():
            return super(CheckoutPage, self).open(CheckoutPage.url)

    def is_on_page(self):
        return self.driver.current_url == CheckoutPage.url

    @property
    def Table(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, '.dataTable')
        except NoSuchElementException:
            return None

    @property
    def ProductsInOrder(self):
        if self.Table is None:
            return []
        return [x.text for x in self.Table.find_elements(By.CSS_SELECTOR, 'td.item')]

    @property
    def Items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'li.item')

    def remove_first_from_cart(self):
        REMOVE_ITEM = By.CSS_SELECTOR, '.item [name="remove_cart_item"]'
        self.wait.until(EC.element_to_be_clickable(REMOVE_ITEM))
        table = self.Table
        remove = self.driver.find_element(*REMOVE_ITEM)
        remove.click()
        self.wait.until(EC.staleness_of(remove))
        self.wait.until(EC.staleness_of(table))
        return self

    def remove_all(self):
        while self.Items:
            self.remove_first_from_cart()
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'em'), 'There are no items in your cart.'))
