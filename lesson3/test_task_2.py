import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://localhost/litecart/en/'

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(3)
    request.addfinalizer(wd.quit)
    return wd


def test_stickers_availability(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    for product in driver.find_elements(By.CSS_SELECTOR, 'li.product'):
        stickers = product.find_elements(By.CSS_SELECTOR, 'div.sticker')
        assert len(stickers) == 1, "One and only one sticker should be displayed for each item!"
        name = product.find_element(By.CSS_SELECTOR, '.name').text
        manufacturer = product.find_element(By.CSS_SELECTOR, '.manufacturer').text
        sticker = stickers[0].text
        print('Name: {name}, Manufacturer: {manufacturer} sticker is: {sticker}'.format(**locals()))
