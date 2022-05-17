the_internet = 'https://the-internet.herokuapp.com'


def test_has_text(driver):
    driver.get('https://crossbrowsertesting.github.io/')
    assert driver.has_text('Examples')


def test_basic_auth(driver):
    driver.basic_auth(f'{the_internet}/basic_auth', 'admin', 'admin')
    assert 'congratulations' in driver.css_element('div[class=example] p').text.lower()
    driver.basic_auth(f'{the_internet}/digest_auth', 'admin', 'admin')
    assert 'congratulations' in driver.css_element('div[class=example] p').text.lower()


def test_drag_and_drop_alternative(driver):
    driver.get(f'{the_internet}/drag_and_drop')
    drag = driver.css_element('div[id=column-a]')
    drop = driver.css_element('div[id=column-b]')
    driver.drag_and_drop(drag, drop, alternative=True)
    assert driver.css_element('div[id=column-a] header').text.lower() == 'b'
