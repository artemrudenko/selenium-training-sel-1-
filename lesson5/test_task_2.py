import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def test_menu_activation(driver):
    driver.get(url)
    find_element, find_elements = driver.find_element, driver.find_elements
    find_element(*Locators.LOGIN).send_keys(login)
    find_element(*Locators.PWD).send_keys(pwd)
    find_element(*Locators.SUBMIT).click()