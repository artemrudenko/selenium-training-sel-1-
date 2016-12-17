from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.page_w_cart import PageWCart


class HomePage(PageWCart):
    url = "http://localhost/litecart/en/"
    # url = "http://192.168.1.5/litecart/en/"

    def open(self):
        if not self.is_on_page():
            return super(HomePage, self).open(HomePage.url)

    def is_on_page(self):
        return self.driver.current_url == HomePage.url

    def goto_product_page(self, category, product):
        if category.lower() == 'popular':
            box_id = 'box-most-popular'
        elif category.lower() == 'campaigns':
            box_id = 'box-campaigns'
        else:
            box_id = 'box-latest-products'
        box = self.driver.find_element(By.ID, box_id)
        box.find_element(By.XPATH, "//li[contains(@class, 'product')]/a/div[contains(., '" + product + "')]").click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'box-product')))
