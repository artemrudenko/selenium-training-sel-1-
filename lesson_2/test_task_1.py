import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # wd = webdriver.Firefox(firefox_binary=r'c:\Program Files\Firefox Nightly\firefox.exe');
    # wd = webdriver.Firefox(capabilities={"marionette": False},
    #                        firefox_binary=r'c:\Program Files (x86)\Mozilla Firefox ESR\firefox.exe')
    # wd = webdriver.Firefox(capabilities={"marionette": True})
    # wd = webdriver.Firefox(capabilities={"marionette": False})
    wd = webdriver.Chrome(desired_capabilities={'chromeOptions': {'args': ["--start-fullscreen"]}})
    wd.implicitly_wait(10)
    # wd = webdriver.Ie()#capabilities={'proxy': {'proxyType': 'manual', 'httpProxy': 'http://10.6.0.1:3128',
                                    #           'sslProxy': 'http://10.6.0.1:3128', 'socksProxy': 'http://10.6.0.1:3128'},
                                    # 'ie.usePerProcessProxy': True})
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get('http://www.google.com/')
    driver.find_element_by_name('q').send_keys('webdriver')
    driver.find_element_by_name('btnK').click()
    WebDriverWait(driver, 10).until(EC.title_is('webdriver - Пошук Google'))
    wait = WebDriverWait(driver, 10) # seconds
    element = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    driver.add_cookie({'name': 'test', 'test': 'bar'})
    test_cookie = driver.get_cookie('test')
    print('test_cookie ' + str(test_cookie))
    cookies = driver.get_cookies()
    print('cookies ' + str(cookies))
    driver.delete_cookie('test')
    driver.delete_all_cookies()
