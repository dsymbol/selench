from selenium.webdriver import Keys

duck = "https://duckduckgo.com"


def test_get_url(driver):
    driver.get(duck)
    assert "duckduckgo" in driver.title.lower()
    assert driver.url == duck


def test_css_elements(driver):
    KEYWORD = "husky"
    driver.get(duck)
    driver.css_element('#search_form_input_homepage').send_keys(KEYWORD, Keys.ENTER)
    results = driver.css_elements('div[id=links] article h2 span')
    for i in results:
        assert KEYWORD in i.text.lower()


def test_xpath_elements(driver):
    KEYWORD = "shiba"
    driver.get(duck)
    driver.xpath_element('//input[@id="search_form_input_homepage"]').send_keys(KEYWORD, Keys.ENTER)
    results = driver.xpath_elements('//div[@id="links"] //article //h2 //span')
    for i in results:
        assert KEYWORD in i.text.lower()


def test_window_geometry(driver):
    driver.get(duck)
    driver.set_window_position(50, 50)
    driver.set_window_size(1000, 1000)
    geo = driver.get_window_geometry()
    assert geo.get("height") == 1000
    assert geo.get("width") == 1000
    assert geo.get("x") == 50
    assert geo.get("y") == 50
