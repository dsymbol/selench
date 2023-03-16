from selench import Keys

import shared


def test_get_url(driver):
    driver.get(shared.DUCK)
    assert "duckduckgo" in driver.title.lower()
    assert shared.DUCK in driver.url


def test_css_elements(driver):
    keyword = "husky"
    driver.get(shared.DUCK)
    driver.css_element('#search_form_input_homepage').send_keys(keyword, Keys.ENTER)
    results = driver.css_elements('div[id=links] article h2 span')
    for i in results:
        assert keyword in i.text.lower()


def test_xpath_elements(driver):
    keyword = "shiba"
    driver.get(shared.DUCK)
    driver.xpath_element('//input[@id="search_form_input_homepage"]').send_keys(keyword, Keys.ENTER)
    results = driver.xpath_elements('//div[@id="links"] //article //h2 //span')
    for i in results:
        assert keyword in i.text.lower()


def test_select_element(driver):
    driver.get(f'{shared.CBT}/selenium_example_page.html')
    select_element = driver.css_element('#dropdown')
    sel = driver.select_element(select_element)
    sel.select_by_value('option2')
    assert driver.css_element('option[value=option2]').is_selected()
    sel.select_by_index(2)
    assert driver.css_element('option[value=option3]').is_selected()


def test_window_geometry(driver):
    driver.get(shared.DUCK)
    driver.set_window_position(50, 50)
    driver.set_window_size(1000, 1000)
    geo = driver.get_window_geometry()
    assert geo.get("height") == 1000
    assert geo.get("width") == 1000
    assert geo.get("x") == 50
    assert geo.get("y") == 50
