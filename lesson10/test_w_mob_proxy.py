# coding: utf8

import logging

import pytest
from hamcrest import assert_that, empty

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


URL = 'http://localhost/litecart/admin/'
PRODUCT_URL = 'http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1'


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
    try:
        from browsermobproxy import Server
        # TODO change to relative path
        server = Server("d:/EDUCATION/SELENIUM/TOOLS/browsermob-proxy-2.1.2/bin/browsermob-proxy")
        server.start()
        proxy = server.create_proxy()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        drv = webdriver.Chrome(chrome_options=chrome_options)
        proxy.new_har("litecart")
    except ImportError:
        drv = webdriver.Chrome()
        proxy = None
    # Ext proxy(fiddler)
    # drv = webdriver.Chrome(desired_capabilities={"proxy": {"proxyType": "MANUAL", "httpProxy": "localhost:8888"}})
    _helper = Helper(drv)
    yield _helper
    try:
        if proxy:
            for x in proxy.har.get('log').get('entries'):
                assert int(x.get('response').get('status')) in (200, 302), "Wrong status for {}".format(x)
    finally:
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
    logger.debug('Available log types: {}'.format(driver.wd.log_types))
    open_products_page(driver)
    links = get_products_links(driver)
    for href in links:
        open_products_page(driver)
        init_product_edit_by_href(driver, href)
        assert_that(driver.wd.get_log("browser"), empty(), "Browser log should be empty")


def get_products_links(drv):
    # not(i) to skip 'Edit' link
    locator = By.XPATH, '//a[contains(@href, "product_id") and not(i)]'
    return [el.get_attribute('href') for el in drv.wd.find_elements(*locator)]


def open_products_page(drv):
    drv.wd.get(PRODUCT_URL)


def init_product_edit_by_href(drv, href):
    product = drv.wd.find_element(By.XPATH, '//a[@href="' + href + '" and not(i)]')
    logger.info("Opening: '{}' href: {}".format(product.text, href))
    product.click()
