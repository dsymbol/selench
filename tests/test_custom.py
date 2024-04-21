from selench import Keys

import shared


def test_basic_auth(driver):
    driver.basic_auth(f'{shared.INTERNET}/basic_auth', 'admin', 'admin')
    assert 'congratulations' in driver.css_element('div[class=example] p').text.lower()
    driver.basic_auth(f'{shared.INTERNET}/digest_auth', 'admin', 'admin')
    assert 'congratulations' in driver.css_element('div[class=example] p').text.lower()


def test_detect_elements(driver):
    keyword = "husky"
    driver.get(shared.DUCK)
    driver.element('input[placeholder]').send_keys(keyword, Keys.ENTER)
    results = driver.elements('article h2 span')
    for i in results:
        assert keyword in i.text.lower()


def test_locator_type(driver):
    css_examples = ['.foo:empty', '#foo', '#foo p', '.foo[bar^="fum"]', 'a:visited', 'h2', '.foo[bar*="fum"]']
    xpath_examples = ['//hr[@class="edge" and position()=1]', './div/b', '//a/@href', '//*[count(*)=3]', '//E/*[1]']
    css_test = [driver._detect_locator_type(i) for i in css_examples]
    xpath_test = [driver._detect_locator_type(i) for i in xpath_examples]
    assert all(["css" in i[0] for i in css_test])
    assert all(["xpath" in i[0] for i in xpath_test])


def test_element_exist_visible(driver):
    driver.get("https://github.com")
    selector = '.text-right [aria-label="Toggle navigation"]'
    assert driver.elements_exist(selector)
    assert driver.elements_visible(selector)
    driver.maximize()
    assert not driver.elements_visible(selector)
