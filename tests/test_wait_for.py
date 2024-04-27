import shared


def test_element_visibility(driver):
    driver.get(f"{shared.INTERNET}/dynamic_loading/2")
    driver.element('div[id="start"] button').click()
    driver.wait_for.element_visibility('div[id="finish"] h4')
    assert "hello world" in driver.element('div[id="finish"] h4').text.lower()
    driver.get(f"{shared.INTERNET}/dynamic_loading/1")
    driver.element('div[id="start"] button').click()
    driver.wait_for.element_invisibility('div[id="loading"]')
    assert not driver.element('div[id="loading"]').is_displayed()


def test_selection_state(driver):
    driver.get(f"{shared.INTERNET}/checkboxes")
    chk1 = driver.element('input[type="checkbox"]').click()
    driver.wait_for.element_selection_state('input[type="checkbox"]', True)
    assert chk1.is_selected()
    chk2 = driver.element('(//input[@type="checkbox"])[2]').click()
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
