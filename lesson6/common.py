from datetime import datetime, date

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def switch_tab(drv, tabText):
    drv.find_element(By.CLASS_NAME, 'tabs').find_element_by_partial_link_text(tabText).click()


def typeIn(element, value):
    element.clear()
    element.send_keys(value)


def selectFrom(element, value):
    select = Select(element)
    return select.select_by_visible_text(value)


def set_datepicker(drv, cssSelector, value):
    drv.execute_script("$('{0}').datepicker('setDate', '{1}')", cssSelector, value)


def set_datetime(drv, name, value):
    if isinstance(value, datetime):
        value = value.strftime('%Y-%m-%dT%H:%M')
    elif isinstance(value, date):
        value = value.strftime('%Y-%m-%d')
    element = drv.find_element_by_name(name)
    drv.execute_script("arguments[0].value=arguments[1]", element, value)


def include_table_rows_by_value(drv, header, items):
    tableLocator = "//td/strong[contains(.,'{header}')]/following-sibling::div[@class='input-wrapper']".format(header=header)
    table = drv.find_element_by_xpath(tableLocator)
    for item in items:
        locator = ".//td[contains(.,'{text}')]/preceding-sibling::td/input[@type='checkbox']".format(text=item)
        table.find_element_by_xpath(locator).click()


def getColumnIndex(table, text):
    locator = './/th[contains(., "{text}")]/preceding-sibling::th'
    return len(table.find_elements(By.XPATH, locator.format(text=text))) + 1


def get_table_column_values(table, column, child=None):
    index = getColumnIndex(table, column)
    assert index != -1, '{column} column was not found!'.format(column=column)
    locator = 'tr.row td:nth-of-type({index})'.format(index=index) + ((' ' + child) if child else '')
    return [el.text for el in table.find_elements(By.CSS_SELECTOR, locator)]
