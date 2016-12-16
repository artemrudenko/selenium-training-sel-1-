from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.page_w_cart import PageWCart
from selenium.webdriver.support import expected_conditions as EC


class ProductPage(PageWCart):

    def open(self):
        raise NotImplementedError

    @property
    def SizeSelect(self):
        try:
            return self.driver.find_element(By.NAME, 'options[Size]')
        except NoSuchElementException:
            return None

    @property
    def QuantityInput(self):
        return self.driver.find_element(By.NAME, 'quantity')

    @property
    def AddButton(self):
        locator = (By.NAME, 'add_cart_product')
        self.wait.until(EC.element_to_be_clickable(locator))
        return self.driver.find_element(*locator)

    def select_size(self, size):
        element = self.SizeSelect
        if element is None or size is None:
            return self
        select = Select(element)
        select.select_by_visible_text(size)
        return self

    def set_quantity(self, quantity):
        self.QuantityInput.clear()
        self.QuantityInput.send_keys(quantity)
        return self

    def add_to_cart(self, quantity, size):
        # TODO think what if quantity <= 0, add assert? or check notification
        self.set_quantity(quantity).select_size(size).submit_add(quantity)
        return self

    def submit_add(self, quantity):
        before = self.get_quantity()
        self.AddButton.click()
        self.wait.until(lambda d: int(self.get_quantity()) == before + quantity)
        return self
