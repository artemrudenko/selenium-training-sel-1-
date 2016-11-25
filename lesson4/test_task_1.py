import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'
    TABLE = By.CLASS_NAME, 'dataTable'
    ROW = By.CLASS_NAME, 'row'
    SELECTED_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected'
    CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li'
    SELECTED_CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li.selected'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def init(drv):
    drv.get(url)
    drv.find_element(*Locators.LOGIN).send_keys(login)
    drv.find_element(*Locators.PWD).send_keys(pwd)
    drv.find_element(*Locators.SUBMIT).click()


def getColumnIndex(drv, text):
    for i, el in enumerate(drv.find_elements(By.TAG_NAME, "th")):
        if el.text == text:
            return i+1
    return -1


def test_countries_sort(driver):
    wait = WebDriverWait(driver, 10)
    init(driver)
    find_element, find_elements = driver.find_element, driver.find_elements
    countryNameIndex = getColumnIndex(driver, 'Name')
    assert countryNameIndex != -1, 'Name column was not found!'
    locator = 'tr.row td:nth-of-type({index})'.format(index=countryNameIndex)
    countries = [el.text for el in find_elements(By.CSS_SELECTOR, locator)]
    assert countries == sorted(countries)


def test_multizones_coutries_sort(driver):
    wait = WebDriverWait(driver, 10)
    init(driver)
    find_element, find_elements = driver.find_element, driver.find_elements
    countryNameIndex = getColumnIndex(driver, 'Name')
    assert countryNameIndex != -1, 'Name column was not found!'
    zonesIndex = getColumnIndex(driver, 'Zones')
    assert zonesIndex != -1, 'Zones column was not found!'
    locator = 'tr.row td:nth-of-type({index})'.format(index=countryNameIndex)
    zlocator = 'tr.row td:nth-of-type({index})'.format(index=zonesIndex)
    countries = filter(lambda pair: int(pair[1]) != 0,
                       zip([el.text for el in find_elements(By.CSS_SELECTOR, locator)],
                           [el.text for el in find_elements(By.CSS_SELECTOR, zlocator)]))
    for x, y in countries:
        print(x, y)
