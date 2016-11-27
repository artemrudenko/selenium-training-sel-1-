from contextlib import contextmanager

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


login, pwd = 'admin', 'admin'

COUNTRIES_URL = 'http://localhost/litecart/admin/?app=countries&doc=countries'
GEO_ZONES = 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'
    TABLE = By.CLASS_NAME, 'dataTable'
    TABLE_ZONES = By.ID, 'table-zones'
    CANCEL = By.CSS_SELECTOR, '.button-set button[name="cancel"]'
    NTH_ROW = By.CSS_SELECTOR, '.dataTable tr.row:nth-of-type({rowId})'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def init(drv, url):
    drv.get(url)
    drv.find_element(*Locators.LOGIN).send_keys(login)
    drv.find_element(*Locators.PWD).send_keys(pwd)
    drv.find_element(*Locators.SUBMIT).click()


def getColumnIndex(table, text):
    for i, el in enumerate(table.find_elements(By.TAG_NAME, "th")):
        if el.text == text:
            return i+1
    return -1


def getColumnIndex2(table, text):
    locator = './/th[contains(., "{text}")]/preceding-sibling::th'
    return len(table.find_elements(By.XPATH, locator.format(text=text))) + 1


def get_table_column_values(table, column, child=None):
    index = getColumnIndex2(table, column)
    assert index != -1, '{column} column was not found!'.format(column=column)
    locator = 'tr.row td:nth-of-type({index})'.format(index=index) + ((' ' + child) if child else '')
    return [el.text for el in table.find_elements(By.CSS_SELECTOR, locator)]


def test_countries_sort(driver):
    init(driver, COUNTRIES_URL)
    table = driver.find_element(*Locators.TABLE)
    countries = get_table_column_values(table, 'Name')
    assert countries == sorted(countries)


@contextmanager
def cancelling(drv, thing):
    try:
        yield thing
    finally:
        drv.find_element(*Locators.CANCEL).click()


def verify_zone_sorting(drv, child=None):
    tableZ = drv.find_element(*Locators.TABLE_ZONES)
    zones = get_table_column_values(tableZ, 'Name', child)
    assert zones == sorted(zones), "SubZones have to be displayed sorted"


def test_multizones_countries_sort(driver):
    init(driver, COUNTRIES_URL)
    find_element, find_elements = driver.find_element, driver.find_elements
    table = driver.find_element(*Locators.TABLE)
    non_empty_zones = [i for i, v in enumerate(get_table_column_values(table, 'Zones')) if int(v) != 0]
    countryNameIndex = str(getColumnIndex2(table, 'Name'))
    for idx in non_empty_zones:
        rowId = str(idx + 2)
        row = find_element(By.CSS_SELECTOR, 'tr.row:nth-of-type(' + rowId + ')')
        row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(' + countryNameIndex + ') a').click()
        try:
            verify_zone_sorting(driver)
        finally:
            find_element(*Locators.CANCEL).click()


def test_zones_sorting(driver):
    init(driver, GEO_ZONES)
    find_element, find_elements = driver.find_element, driver.find_elements
    table = driver.find_element(*Locators.TABLE)
    countryNameIndex = str(getColumnIndex2(table, 'Name'))
    rowsCount = len(table.find_elements(By.CSS_SELECTOR, 'tr.row'))
    for idx in range(2, rowsCount+2):
        rowId = str(idx)
        row = find_element(By.CSS_SELECTOR, 'tr.row:nth-of-type(' + rowId + ')')
        row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(' + countryNameIndex + ') a').click()
        try:
            verify_zone_sorting(driver, 'select option:checked')
        finally:
            find_element(*Locators.CANCEL).click()
