# coding: utf8

import logging
import time
from datetime import datetime

import pytest
from hamcrest import assert_that, empty

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/admin/'


class Listener(AbstractEventListener):
    def before_find(self, by, value, drv):
        logger.debug('Trying to find by {} : value {}'.format(by, value))

    def after_find(self, by, value, drv):
        logger.debug('Found by {} value {}'.format(by, value))

    def on_exception(self, exception, drv):
        logger.debug(exception)
        fname = 'screen-{0}.png'.format(int(time.mktime(datetime.now().timetuple())))
        drv.get_screenshot_as_file(fname)
        logger.debug('Screenshot saved: {fname}'.format(fname=fname))

    def before_quit(self, drv):
        for l in drv.get_log("browser"):
            logger.info('{}'.format(l))


class Helper(object):
    def __init__(self, drv):
        self._wd = drv
        self._wd.maximize_window()
        self._wait = WebDriverWait(drv, 20)

    @property
    def wd(self):
        return self._wd

    @property
    def wait(self):
        return self._wait


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'


@pytest.yield_fixture
def driver():
    _helper = Helper(EventFiringWebDriver(webdriver.Chrome(), Listener()))
    yield _helper
    _helper.wd.quit()


def init(drv):
    drv.wd.get(URL)
    email, password = 'admin', 'admin'
    drv.wd.find_element(*Locators.LOGIN).send_keys(email)
    drv.wd.find_element(*Locators.PWD).send_keys(password)
    drv.wd.find_element(*Locators.SUBMIT).click()


def test_browser_logs_on_product_opening(driver):
    """
        Сделайте сценарий, который проверяет, не появляются ли сообщения об ошибках при открытии страниц в учебном
        приложении, а именно -- страниц товаров в каталоге в административной панели.

        Сценарий должен состоять из следующих частей:
            #) зайти в админку
            #) открыть каталог, категорию, которая содержит товары (страница http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1)
            #) последовательно открывать страницы товаров и проверять, не появляются ли в логе браузера сообщения об ошибках (любого уровня критичности)
    """
    init(driver)
    driver.wd.get('http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1')
    unique = set(link.get_attribute('href') for link in driver.wd.find_elements(By.XPATH,
                                                                                '//a[contains(@href, "product_id")]'))
    logger.info("Total unique links(products): {}".format(len(unique)))
    for href in unique:
        driver.wd.get('http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1')
        product = driver.wd.find_elements(By.XPATH, '//a[@href="' + href + '"]')[0]
        logger.info("Opening: '{}'".format(product.text))
        product.click()
