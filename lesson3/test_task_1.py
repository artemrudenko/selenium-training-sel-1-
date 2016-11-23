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
    HEADER = By.TAG_NAME, 'h1'
    MENU_ITEM = By.CSS_SELECTOR, 'li#app-'
    SELECTED_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected'
    CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li'
    SELECTED_CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li.selected'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_1(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    find_element, find_elements = driver.find_element, driver.find_elements
    find_element(*Locators.LOGIN).send_keys(login)
    find_element(*Locators.PWD).send_keys(pwd)
    find_element(*Locators.SUBMIT).click()
    for i, root in enumerate([x.text for x in find_elements(*Locators.MENU_ITEM)]):
        find_elements(*Locators.MENU_ITEM)[i].click()
        wait.until(EC.presence_of_element_located(Locators.SELECTED_MENU_ITEM) and
                   EC.text_to_be_present_in_element(Locators.SELECTED_MENU_ITEM, root))
        active = find_element(*Locators.SELECTED_MENU_ITEM)
        assert active.text.startswith(root), 'After menu item click it should become selected!'
        for j, child in enumerate([x.text for x in find_elements(*Locators.CHILD_MENU_ITEM)]):
            sub_menu = find_elements(*Locators.CHILD_MENU_ITEM)[j]
            sub_menu.click()
            wait.until(EC.presence_of_element_located(Locators.SELECTED_CHILD_MENU_ITEM) and
                       EC.text_to_be_present_in_element(Locators.SELECTED_CHILD_MENU_ITEM, child))
            active_child = find_element(*Locators.SELECTED_CHILD_MENU_ITEM)
            assert active_child.text == child, 'After sub-menu item click it should become selected!'
            assert find_elements(*Locators.HEADER) != []
        else:
            assert find_elements(*Locators.HEADER) != []
