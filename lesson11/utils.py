from selenium.webdriver.support.select import Select


def selectFrom(element, value):
    if value:
        select = Select(element)
        return select.select_by_visible_text(value)


def is_element_present(drv, locator):
    return len(drv.find_elements(*locator)) > 0


def is_element_not_present(drv, locator):
    try:
        drv.implicitly_wait(0)
        return len(drv.find_elements(*locator)) > 0
    finally:
        drv.implicitly_wait(10)
