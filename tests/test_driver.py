import shared


def test_get_url(driver):
    driver.get(shared.DUCK)
    assert "duckduckgo" in driver.title.lower()
    assert shared.DUCK in driver.url


def test_select_element(driver):
    driver.get(f'{shared.CBT}/selenium_example_page.html')
    sel = driver.element('#dropdown')
    sel.select_by_value('option2')
    assert driver.element('option[value=option2]').is_selected()
    sel.select_by_index(2)
    assert driver.element('option[value=option3]').is_selected()


def test_window_geometry(driver):
    driver.get(shared.DUCK)
    driver.set_window_position(50, 50)
    driver.set_window_size(1000, 1000)
    geo = driver.get_window_geometry()
    assert geo.get("height") == 1000
    assert geo.get("width") == 1000
    assert geo.get("x") == 50
    assert geo.get("y") == 50
