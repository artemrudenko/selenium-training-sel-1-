import random

import logging
from functools import wraps

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import is_element_present
from utils import selectFrom

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/en/'
wait = None


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


class Locators(object):
    POPULAR = By.ID, 'box-most-popular'
    PRODUCTS = By.CLASS_NAME, 'products'
    REMOVE = By.NAME, 'remove_cart_item'
    SIZE = By.NAME, 'options[Size]'
    CART_QUANTITY = By.CSS_SELECTOR, '#cart .quantity'
    ADD_TO_CART = By.NAME, 'add_cart_product'
    REMOVE_FROM_CART = By.NAME, 'remove_cart_item'
    CHECKOUT = By.PARTIAL_LINK_TEXT, 'Checkout'
    HOME = By.CLASS_NAME, 'fa-home'
    CART_TEXT = By.TAG_NAME, 'em'
    TABLE = By.CLASS_NAME, 'dataTable'
    REMOVE_ITEM = By.CSS_SELECTOR, '.item [name="remove_cart_item"]'


@pytest.yield_fixture
def driver():
    global wait
    _wd = webdriver.Chrome()
    wait = WebDriverWait(_wd, 20)
    yield _wd
    _wd.quit()
    wait = None


def test_product_opening(driver):
    driver.get(URL)
    for candidate in generate_candidates(driver):
        add_product_to_cart(driver, candidate)
    goto_checkout(driver)
    while driver.find_elements(By.CSS_SELECTOR, 'li.item'):
        remove_first_product_from_cart(driver)
    wait.until(EC.text_to_be_present_in_element(Locators.CART_TEXT, 'There are no items in your cart.'))
    assert wait.until(EC.text_to_be_present_in_element(Locators.CART_TEXT, 'There are no items in your cart.')), \
        "Empty cart text missed"


def generate_candidates(drv):
    box = drv.find_element(*Locators.POPULAR)
    available = [el.text for el in box.find_elements(By.CLASS_NAME, 'name')]
    return random.sample(available, min(len(available), 3))


def goto_checkout(drv):
    drv.find_element(*Locators.CHECKOUT).click()
    wait.until(EC.title_is('Checkout | My Store'))


def goto_home(drv):
    drv.find_element(*Locators.HOME).click()
    wait.until(EC.title_is('Online Store | My Store'))


def open_product(drv, product):
    # currently adding product only from the popular category
    box = drv.find_element(*Locators.POPULAR)
    box.find_element(By.XPATH, "//li[contains(@class, 'product')]/a/div[contains(., '" + product + "')]").click()
    wait.until(EC.presence_of_element_located((By.ID, 'box-product')))


@log
def add_product_to_cart(drv, product):
    logger.info("Going add product: {product}".format(product=product))
    before = int(drv.find_element(*Locators.CART_QUANTITY).text)
    open_product(drv, product)
    if is_element_present(drv, Locators.SIZE):
        selectFrom(drv.find_element(*Locators.SIZE), 'Small')
    wait.until(EC.element_to_be_clickable(Locators.ADD_TO_CART))
    drv.find_element(*Locators.ADD_TO_CART).click()
    wait.until(lambda d: d.find_element(*Locators.CART_QUANTITY).text == str(before + 1))
    goto_home(drv)


def remove_first_product_from_cart(drv):
    wait.until(EC.element_to_be_clickable(Locators.REMOVE_ITEM))
    table = drv.find_element(*Locators.TABLE)
    remove = drv.find_element(*Locators.REMOVE_ITEM)
    remove.click()
    wait.until(EC.staleness_of(remove))
    wait.until(EC.staleness_of(table))
