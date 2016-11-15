import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://localhost/litecart/admin/'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = 'username'
    PWD = 'password'
    SUBMIT = 'login'
    REMEMBER = 'remember_me'
    NOTICES = 'notices-wrapper'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def get_text(elements):
    if isinstance(elements, list):
        return [el.text.strip() for el in elements]
    return elements.text.strip()


def get_notices(drv):
    out = {}
    element = drv.find_element_by_id(Locators.NOTICES)
    style = element.get_attribute('style')
    if style != '':
        return out
    for status in ('success', 'warnings', 'errors'):
        try:
            out[status] = get_text(element.find_elements_by_css_selector('.notice.{status}'.format(status=status)))
        except NoSuchElementException:
            pass
    return out


def configure(drv, login_value=None, pwd_value=None, remember=None):
    if login_value is not None:
        drv.find_element_by_name(Locators.LOGIN).send_keys(login_value)
    if pwd_value is not None:
        drv.find_element_by_name(Locators.PWD).send_keys(pwd_value)
    if remember:
        drv.find_element_by_name(Locators.REMEMBER).click()
    drv.find_element_by_name(Locators.SUBMIT).click()
    return get_notices(drv)


def test_wo_login_and_pwd(driver):
    driver.get(url)
    errors = configure(driver).get('errors')
    assert errors[0] == 'You must provide a username'


def test_wo_login(driver):
    driver.get(url)
    errors = configure(driver, pwd_value=pwd).get('errors')
    assert errors[0] == 'You must provide a username'


def test_wo_pwd(driver):
    driver.get(url)
    errors = configure(driver, login_value=login).get('errors')
    assert 'Wrong combination of username and password or the account does not exist.' in errors


def test_login(driver):
    driver.get(url)
    notices = configure(driver, login_value=login, pwd_value=pwd)
    assert notices['errors'] == [], 'No errors'
    assert notices['success'] == ['You are now logged in as admin']


def test_remember_me(driver):
    driver.get(url)
    notices = configure(driver, login_value=login, pwd_value=pwd, remember=True)
    assert notices['errors'] == [], 'No errors'
    assert notices['success'] == ['You are now logged in as admin']


def test_logo_click_redirect(driver):
    driver.get(url)
    driver.find_element_by_tag_name('a').click()
    WebDriverWait(driver, 10).until(EC.title_is('Online Store | My Store'))
