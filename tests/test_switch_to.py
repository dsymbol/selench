the_internet = 'https://the-internet.herokuapp.com'
duck = 'https://duckduckgo.com'


def test_new_window(driver):
    driver.get(duck)
    windows = len(driver.all_window_handles)
    driver.new_window()
    assert len(driver.all_window_handles) == windows + 1


def test_new_tab(driver):
    driver.get(duck)
    tabs = len(driver.all_window_handles)
    driver.new_tab()
    assert len(driver.all_window_handles) == tabs + 1


def test_switch_window(driver):
    driver.get(duck)
    first_window = driver.current_window_handle
    driver.new_window()
    assert driver.current_window_handle != first_window
    driver.switch_window(name=first_window)
    assert driver.current_window_handle == first_window


def test_switch_frame(driver):
    driver.get(f"{the_internet}/iframe")
    frame = driver.css_element('iframe[id=mce_0_ifr]')
    driver.switch_frame(frame)
    textarea = driver.css_element('body')
    textarea.clear()
    textarea.send_keys('tests')
    assert textarea.text == 'tests'
    driver.leave_frame()
    assert driver.css_element('iframe[id=mce_0_ifr]')


def test_alert(driver):
    driver.get(f"{the_internet}/javascript_alerts")
    result = driver.css_element('#result')
    driver.css_element('button[onclick*=Alert]').click()
    driver.alert().dismiss()
    assert result.text.lower() == "you successfully clicked an alert"
    driver.css_element('button[onclick*=Confirm]').click()
    driver.alert().accept()
    assert result.text.lower() == "you clicked: ok"
    driver.css_element('button[onclick*=Prompt]').click()
    driver.alert().send_keys('tests')
    driver.alert().accept()
    assert result.text.lower() == "you entered: tests"