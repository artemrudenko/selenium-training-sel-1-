import random
import pytest
import logging

from datetime import date, timedelta, datetime
from faker import Factory
from functools import wraps
from hamcrest import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from common import switch_tab, typeIn, include_table_rows_by_value, selectFrom, set_datetime, get_table_column_values


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


fake = Factory.create()
url = 'http://localhost/litecart/admin/'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def init(drv, email, password):
    drv.get(url)
    drv.find_element(By.NAME, 'username').send_keys(email)
    drv.find_element(By.NAME, 'password').send_keys(password)
    drv.find_element(By.NAME, 'login').click()


def test_add_product(driver):
    init(driver, login, pwd)
    select_menu(driver, 'Catalog')
    before = get_table_column_values(driver.find_element_by_class_name('dataTable'), 'Name')
    logger.debug('Products before: {before}'.format(before=before))

    init_product_creation(driver)
    name = fake.name()
    logger.debug("adding product with name: {name}".format(name=name))
    fill_general_info(driver, True, name=name, code=fake.ean8(), quantity=random.randint(1, 100),
                      dateValidFrom=(date.today() + timedelta(days=random.randint(1, 10))).strftime('%m%d%Y'),
                      dateValidTo=(date.today() + timedelta(days=random.randint(20, 100))).strftime('%m%d%Y'))
    fill_information(driver, manufacturer='ACME Corp.', keywords=fake.words(nb=3),
                     shortDescription=fake.text(max_nb_chars=50),
                     description=fake.paragraphs(nb=3), title=fake.word() + ' Duck')
    usdPrice = random.randint(1, 100)
    fill_prices(driver, purchasePrice=random.randint(1, 100), ccy='US Dollars', usdPrice=usdPrice,
                campaigns=[{'startDate': datetime.today() + timedelta(days=random.randint(1, 10)),
                            'endDate': datetime.today() + timedelta(days=random.randint(20, 100)),
                            'usd': random.randint(1, usdPrice)}])
    success = save_changes(driver)
    assert success, "No any errors notifications should be visible!"
    products = get_table_column_values(driver.find_element_by_class_name('dataTable'), 'Name')
    logger.debug('Products after: {products}'.format(products=products))
    assert_that(products, has_item(name), "Added product should be visible")


def save_changes(drv):
    drv.find_element_by_name('save').click()
    return drv.find_elements_by_css_selector('notice-wrapper .error') == []


@log
def fill_general_info(drv, enabled, name, code, quantity, dateValidFrom, dateValidTo):
    switch_tab(drv, 'General')
    value = '1' if enabled else '0'
    drv.find_element_by_css_selector("input[type='radio'][value='{value}']".format(value=value)).click()
    typeIn(drv.find_element_by_name('name[en]'), name)
    typeIn(drv.find_element_by_name('code'), code)
    include_table_rows_by_value(drv, 'Categories', ['Subcategory'])
    include_table_rows_by_value(drv, 'Product Groups', ['Male', 'Female'])
    typeIn(drv.find_element_by_name('quantity'), quantity)
    drv.find_element_by_name('date_valid_from').send_keys(dateValidFrom)
    drv.find_element_by_name('date_valid_to').send_keys(dateValidTo)


@log
def fill_prices(drv, purchasePrice, ccy, usdPrice, campaigns=None):
    switch_tab(drv, 'Prices')
    typeIn(drv.find_element_by_name('purchase_price'), purchasePrice)
    selectFrom(drv.find_element_by_name('purchase_price_currency_code'), ccy)
    typeIn(drv.find_element_by_name('prices[USD]'), usdPrice)
    for campaign in campaigns:
        add_campaign(drv, **campaign)


@log
def fill_information(drv, manufacturer, keywords, shortDescription, description, title):
    switch_tab(drv, 'Information')
    selectFrom(drv.find_element_by_name('manufacturer_id'), manufacturer)
    typeIn(drv.find_element_by_name('keywords'), keywords)
    typeIn(drv.find_element_by_name('short_description[en]'), shortDescription)
    typeIn(drv.find_element_by_class_name('trumbowyg-editor'), description)
    typeIn(drv.find_element_by_name('head_title[en]'), title)


def init_product_creation(drv):
    drv.find_element_by_partial_link_text('Add New Product').click()


def select_menu(drv, text):
    for el in drv.find_elements(By.CSS_SELECTOR, 'li#app-'):
        if el.text == text:
            el.click()
            break


@log
def add_campaign(drv, startDate, endDate, usd):
    table = drv.find_element_by_id('table-campaigns')
    before = len(table.find_elements_by_tag_name('tr'))
    table.find_element_by_id('add-campaign').click()
    prefix = "campaigns[new_{index}]".format(index=before)
    set_datetime(drv, prefix + "[start_date]", startDate)
    set_datetime(drv, prefix + "[end_date]", endDate)
    typeIn(table.find_element_by_name(prefix + '[USD]'), usd)
