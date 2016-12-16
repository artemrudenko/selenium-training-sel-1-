# coding: utf8

import logging
from functools import wraps

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/admin/'


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


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'
    EXT_LINK = By.CLASS_NAME, 'fa-external-link'


@pytest.yield_fixture
def driver():
    _helper = Helper(webdriver.Chrome())
    yield _helper
    _helper.wd.quit()


def init(drv):
    drv.wd.get(URL)
    email, password = 'admin', 'admin'
    drv.wd.find_element(*Locators.LOGIN).send_keys(email)
    drv.wd.find_element(*Locators.PWD).send_keys(password)
    drv.wd.find_element(*Locators.SUBMIT).click()


def select_menu(drv, text):
    xpath = '//*[@class="name" and text()="{text}"]/ancestor::li[@id="app-"]'.format(text=text)
    drv.wd.find_element(By.XPATH, xpath).click()


def test_open_external_links(driver):
    """
        Cделайте сценарий, который проверяет, что ссылки на странице редактирования страны открываются в новом окне.

        Сценарий должен состоять из следующих частей:
            #) зайти в админку
            #) открыть пункт меню Countries (или страницу http://localhost/litecart/admin/?app=countries&doc=countries)
            #) открыть на редактирование какую-нибудь страну или начать создание новой
            #) возле некоторых полей есть ссылки с иконкой в виде квадратика со стрелкой -- они ведут на внешние страницы и открываются в новом окне, именно это и нужно проверить.
    """
    init(driver)
    select_menu(driver, 'Countries')
    init_add_country(driver)
    for link in driver.wd.find_elements(*Locators.EXT_LINK):
        main_window = driver.wd.current_window_handle
        goto_external(driver, link)
        close_active_window(driver)
        goto_window(driver, main_window)


def close_active_window(drv):
    drv.wd.close()


def goto_external(drv, element):
    old_windows = drv.wd.window_handles
    element.click()
    drv.wait.until(EC.new_window_is_opened(old_windows))
    new_window = [x for x in drv.wd.window_handles if x not in old_windows].pop()
    goto_window(drv, new_window)


def goto_window(drv, handle):
    drv.wd.switch_to_window(handle)
    logger.info("Title is: {}".format(drv.wd.title))


def init_add_country(drv):
    drv.wd.find_element_by_partial_link_text('Add New Country').click()
    drv.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Add New Country'))
