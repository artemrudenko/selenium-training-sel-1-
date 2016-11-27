import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'
    TABLE = By.CLASS_NAME, 'dataTable'
    ROW = By.CLASS_NAME, 'row'


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
    return len(table.find_elements(By.XPATH, './/th[contains(., "{text}")]/preceding-sibling::th'.format(text=text))) + 1


def get_table_column_values(table, column, child=None):
    index = getColumnIndex2(table, column)
    assert index != -1, '{column} column was not found!'.format(column=column)
    locator = 'tr.row td:nth-of-type({index})'.format(index=index) + (' ' + child) if child else ''
    # if child is None:
    return [el.text for el in table.find_elements(By.CSS_SELECTOR, locator)]
    # else:
    #     return [el.getAttribute('value') for el in table.find_elements(By.CSS_SELECTOR, locator)]


def test_countries_sort(driver):
    init(driver, 'http://localhost/litecart/admin/?app=countries&doc=countries')
    table = driver.find_element(By.CSS_SELECTOR, '.dataTable')
    countries = get_table_column_values(table, 'Name')
    assert countries == sorted(countries)


def test_multizones_countries_sort(driver):
    init(driver, 'http://localhost/litecart/admin/?app=countries&doc=countries')
    find_element, find_elements = driver.find_element, driver.find_elements
    table = driver.find_element(By.CSS_SELECTOR, '.dataTable')
    countryNameIndex = getColumnIndex2(table, 'Name')
    # assert countryNameIndex != -1, 'Name column was not found!'
    zonesIndex = getColumnIndex2(table, 'Zones')
    assert zonesIndex != -1, 'Zones column was not found!'
    rowsCount = len(table.find_elements(By.CSS_SELECTOR, 'tr.row'))
    for idx in range(2, rowsCount+2):
        row = find_element(By.CSS_SELECTOR, '.dataTable tr.row:nth-of-type('+str(idx)+')')
        zones = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type('+str(zonesIndex)+')').text
        if int(zones) == 0:
            continue
        try:
            row.find_element(By.CSS_SELECTOR, 'td:nth-of-type('+str(countryNameIndex)+') a').click()
            tableZ = driver.find_element(By.ID, 'table-zones')
            zones = get_table_column_values(tableZ, 'Name')
            assert zones == sorted(zones), "SubZones have to be displayed sorted"
        finally:
            find_element(By.CSS_SELECTOR, '.button-set button[name="cancel"]').click()


def test_zones_sorting(driver):
    init(driver, 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones')
    find_element, find_elements = driver.find_element, driver.find_elements
    table = driver.find_element(By.CSS_SELECTOR, '.dataTable')
    countryNameIndex = getColumnIndex2(table, 'Name')
    rowsCount = len(table.find_elements(By.CSS_SELECTOR, 'tr.row'))
    for idx in range(2, rowsCount+2):
        row = find_element(By.CSS_SELECTOR, '.dataTable tr.row:nth-of-type('+str(idx)+')')
        try:
            row.find_element(By.CSS_SELECTOR, 'td:nth-of-type('+str(countryNameIndex)+') a').click()
            tableZ = driver.find_element(By.ID, 'table-zones')
            zones = get_table_column_values(tableZ, 'Name', 'select option:checked')
            assert zones == sorted(zones), "SubZones have to be displayed sorted"
        finally:
            find_element(By.CSS_SELECTOR, '.button-set button[name="cancel"]').click()
