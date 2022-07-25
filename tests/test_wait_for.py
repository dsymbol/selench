from selenium.webdriver import Keys

import shared


def test_element_visibility(driver):
    driver.get(f"{shared.INTERNET}/dynamic_loading/2")
    driver.element('div[id="start"] button').click()
    elm = driver.wait_for.element_visibility('div[id="finish"] h4')
    assert "hello world" in elm.text.lower()
    driver.get(f"{shared.INTERNET}/dynamic_loading/1")
    driver.element('div[id="start"] button').click()
    elm = driver.wait_for.element_invisibility('div[id="loading"]')
    assert not elm.is_displayed()


def test_elements_visibility(driver):
    driver.get("https://github.com/")
    driver.maximize()
    dd = driver.element('(//summary[contains(@class, "HeaderMenu-summary")])[1]')
    driver.action.hover(dd)
    elements = driver.wait_for.elements_visibility('(//div[contains(@class,"dropdown-menu")])[1] //li')
    assert all([i.is_displayed() for i in elements])
    dd.click()
    elements = driver.wait_for.elements_invisibility('(//div[contains(@class,"dropdown-menu")])[1] //li')
    assert not all([i.is_displayed() for i in elements])


def test_selection_state(driver):
    driver.get(f"{shared.INTERNET}/checkboxes")
    chk1 = driver.element('input[type="checkbox"]')
    chk1.click()
    driver.wait_for.element_selection_state('input[type="checkbox"]', True)
    assert chk1.is_selected()
    chk2 = driver.element('(//input[@type="checkbox"])[2]')
    chk2.click()
    driver.wait_for.element_selection_state('(//input[@type="checkbox"])[2]', False)
    assert not chk2.is_selected()


def test_url_to_be(driver):
    driver.get(shared.INTERNET)
    driver.get(shared.DUCK)
    driver.wait_for.url_to_be(f'{shared.DUCK}/')
    assert driver.url == f'{shared.DUCK}/'


def test_title_to_be(driver):
    title = 'ok at DuckDuckGo'
    driver.get(f"{shared.DUCK}/?q=ok")
    driver.wait_for.title_to_be(title)
    assert driver.title == title
