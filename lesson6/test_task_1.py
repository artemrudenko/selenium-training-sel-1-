import random

import logging
from functools import wraps

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import is_element_present, selectFrom


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/en/'


class Helper(object):
    def __init__(self, drv):
        self._wd = drv
        self._wait = WebDriverWait(drv, 20)

    @property
    def wd(self):
        return self._wd

    @property
    def wait(self):
        return self._wait


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


class Locators(object):
    POPULAR = By.ID, 'box-most-popular'
    SIZE = By.NAME, 'options[Size]'
    CART_QUANTITY = By.CSS_SELECTOR, '#cart .quantity'
    ADD_TO_CART = By.NAME, 'add_cart_product'
    CHECKOUT = By.PARTIAL_LINK_TEXT, 'Checkout'
    HOME = By.CLASS_NAME, 'fa-home'
    CART_TEXT = By.TAG_NAME, 'em'
    TABLE = By.CLASS_NAME, 'dataTable'
    REMOVE_ITEM = By.CSS_SELECTOR, '.item [name="remove_cart_item"]'


@pytest.yield_fixture
def driver():
    _helper = Helper(webdriver.Chrome())
    yield _helper
    _helper.wd.quit()


def test_cart_workflow(driver):
    wd = driver.wd
    wd.get(URL)
    for candidate in generate_candidates(driver):
        add_product_to_cart(driver, candidate)
    goto_checkout(driver)
    while wd.find_elements(By.CSS_SELECTOR, 'li.item'):
        remove_first_product_from_cart(driver)
    driver.wait.until(EC.text_to_be_present_in_element(Locators.CART_TEXT, 'There are no items in your cart.'))
    assert driver.wait.until(EC.text_to_be_present_in_element(Locators.CART_TEXT, 'There are no items in your cart.')), \
        "Empty cart text missed"


def generate_candidates(drv):
    box = drv.wd.find_element(*Locators.POPULAR)
    available = [el.text for el in box.find_elements(By.CLASS_NAME, 'name')]
    return random.sample(available, min(len(available), 3))


def goto_checkout(drv):
    drv.wd.find_element(*Locators.CHECKOUT).click()
    drv.wait.until(EC.title_is('Checkout | My Store'))


def goto_home(drv):
    drv.wd.find_element(*Locators.HOME).click()
    drv.wait.until(EC.title_is('Online Store | My Store'))


def open_product(drv, product):
    # currently adding product only from the popular category
    box = drv.wd.find_element(*Locators.POPULAR)
    box.find_element(By.XPATH, "//li[contains(@class, 'product')]/a/div[contains(., '" + product + "')]").click()
    drv.wait.until(EC.presence_of_element_located((By.ID, 'box-product')))


@log
def add_product_to_cart(drv, product):
    logger.info("Going add product: {product}".format(product=product))
    before = int(drv.wd.find_element(*Locators.CART_QUANTITY).text)
    open_product(drv, product)
    if is_element_present(drv.wd, Locators.SIZE):
        selectFrom(drv.wd.find_element(*Locators.SIZE), 'Small')
    drv.wait.until(EC.element_to_be_clickable(Locators.ADD_TO_CART))
    drv.wd.find_element(*Locators.ADD_TO_CART).click()
    drv.wait.until(lambda d: d.find_element(*Locators.CART_QUANTITY).text == str(before + 1))
    goto_home(drv)


def remove_first_product_from_cart(drv):
    drv.wait.until(EC.element_to_be_clickable(Locators.REMOVE_ITEM))
    table = drv.wd.find_element(*Locators.TABLE)
    remove = drv.wd.find_element(*Locators.REMOVE_ITEM)
    remove.click()
    drv.wait.until(EC.staleness_of(remove))
    drv.wait.until(EC.staleness_of(table))
