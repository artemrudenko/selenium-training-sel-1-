import pytest
from hamcrest import *
from selenium import webdriver
from selenium.webdriver.common.by import By


login, pwd = 'admin', 'admin'
URL = 'http://localhost/litecart/en/'


class Locators(object):
    CAMPAIGNS = By.ID, 'box-campaigns'
    PRODUCT = By.ID, 'box-product'
    REGULAR_PRICE = By.CSS_SELECTOR, '.regular-price'
    CAMPAIGN_PRICE = By.CSS_SELECTOR, '.campaign-price'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_product_opening(driver):
    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))
    homeDetails = {'name': owner.find_element(By.CLASS_NAME, 'name').text,
                   'manufacturer': owner.find_element(By.CSS_SELECTOR, '.manufacturer').text,
                   'regular-price': owner.find_element(*Locators.REGULAR_PRICE).text,
                   'campaign-price': owner.find_element(*Locators.CAMPAIGN_PRICE).text}
    owner.click()

    owner = driver.find_element(*Locators.PRODUCT)
    productDetails = {'name': owner.find_element(By.CLASS_NAME, 'title').text,
                      'manufacturer': owner.find_element(By.CSS_SELECTOR, '.manufacturer img').get_attribute('title'),
                      'regular-price': owner.find_element(*Locators.REGULAR_PRICE).text,
                      'campaign-price': owner.find_element(*Locators.CAMPAIGN_PRICE).text}

    assert_that(productDetails, has_entries(homeDetails),
                "Check that opened product has the same attributes as one user trying to open")


def get_element_style_info(element, props=None):
    cssProperties = props if props is not None else ['color', 'text-decoration', 'font-weight', 'font-size']
    return dict((prop, element.value_of_css_property(prop)) for prop in cssProperties)


def test_campaign_styles(driver):
    expected = {'regular-price-home': {'color': 'rgba(119, 119, 119, 1)', 'text-decoration': 'line-through',
                                       'font-weight': 'normal', 'font-size': '14.4px'},
                'campaign-price-home': {'color': 'rgba(204, 0, 0, 1)', 'text-decoration': 'none',
                                        'font-weight': 'bold', 'font-size': '18px'},
                'regular-price-product': {'color': 'rgba(102, 102, 102, 1)', 'text-decoration': 'line-through',
                                          'font-weight': 'normal', 'font-size': '16px'},
                'campaign-price-product': {'color': 'rgba(204, 0, 0, 1)', 'text-decoration': 'none',
                                           'font-weight': 'bold', 'font-size': '22px'}}

    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))
    displayed = {'regular-price-home': get_element_style_info(owner.find_element(*Locators.REGULAR_PRICE)),
                 'campaign-price-home': get_element_style_info(owner.find_element(*Locators.CAMPAIGN_PRICE))}
    owner.click()

    owner = driver.find_element(*Locators.PRODUCT)
    displayed['regular-price-product'] = get_element_style_info(owner.find_element(*Locators.REGULAR_PRICE))
    displayed['campaign-price-product'] = get_element_style_info(owner.find_element(*Locators.CAMPAIGN_PRICE))

    assert_that(displayed, has_entries(expected), 'Check styles')
