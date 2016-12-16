import pytest
import exrex
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Factory


URL = 'http://localhost/litecart/en/'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def login(drv, email, password):
    drv.find_element(By.NAME, 'email').send_keys(email)
    drv.find_element(By.NAME, 'password').send_keys(password)
    drv.find_element(By.NAME, 'login').click()


def logout(drv):
    drv.find_element(By.LINK_TEXT, 'Logout').click()


def test_product_opening(driver):
    driver.get(URL)
    email, pwd = create_user(driver)
    logout(driver)
    login(driver, email, pwd)
    logout(driver)
    login(driver, email, pwd)


def create_user(drv):
    fake = Factory.create()
    email = fake.safe_email()
    pwd = fake.credit_card_number(card_type=None)
    drv.find_element(By.LINK_TEXT, 'New customers click here').click()
    first, second = fake.name().split()
    drv.find_element(By.NAME, 'firstname').send_keys(first)
    drv.find_element(By.NAME, 'lastname').send_keys(second)
    drv.find_element(By.NAME, 'address1').send_keys(fake.street_address())
    drv.find_element(By.NAME, 'address2').send_keys(fake.street_address())
    country = fake.country()
    for el in drv.find_element(By.NAME, 'country_code').find_elements(By.TAG_NAME, 'option'):
        if country in el.text:
            el.click()
            break
    postcode = drv.find_element(By.NAME, 'postcode')
    postcode.send_keys(exrex.getone(postcode.get_attribute('pattern')))
    drv.find_element(By.NAME, 'city').send_keys(fake.city())
    drv.find_element(By.NAME, 'email').send_keys(email)
    phone = drv.find_element(By.NAME, 'phone')
    phone.send_keys(exrex.getone(phone.get_attribute('pattern')))
    drv.find_element(By.NAME, 'password').send_keys(pwd)
    drv.find_element(By.NAME, 'confirmed_password').send_keys(pwd)
    drv.find_element(By.NAME, 'create_account').click()
    return email, pwd

