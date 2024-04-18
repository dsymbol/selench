import shared


def test_hover(driver):
    driver.get(f'{shared.CBT}/hover-menu.html')
    dd_element = driver.xpath_element('//li[@class="dropdown"] /a')
    driver.hover(dd_element)
    new_visible_elements = driver.xpath_elements('//ul[@class="dropdown-menu"] //li /a[not(@onclick)]')
    assert all([i.is_displayed for i in new_visible_elements])


def test_double_click(driver):
    driver.get('https://www.javatpoint.com/oprweb/test.jsp?filename=javascript-dblclick-event1')
    driver.switch_frame('//iframe[@id="iframewrapper"]')
    dbl_element = driver.xpath_element('//*[@id="heading"]')
    driver.double_click(dbl_element)
    dbl_element = driver.xpath_element('//*[@id="heading"]')
    assert "javatpoint.com" in dbl_element.text.lower()


def test_right_click(driver):
    driver.get(f'{shared.INTERNET}/context_menu')
    rclick_element = driver.css_element('div[id=hot-spot]')
    driver.right_click(rclick_element)
    alert = driver.alert()
    assert alert.text.lower() == 'you selected a context menu'


def test_drag_and_drop(driver):
    expected = 'Dropped!'
    driver.get(f'{shared.CBT}/drag-and-drop.html')
    drag = driver.css_element('#draggable')
    drop = driver.css_element('#droppable')
    driver.drag_and_drop(drag, drop)
    driver.wait_for.element_text_to_be('div[id=droppable] p', expected)
    assert driver.css_element('div[id=droppable] p').text == expected

    driver.get(f'{shared.INTERNET}/drag_and_drop')
    drag = driver.css_element('div[id=column-a]')
    drop = driver.css_element('div[id=column-b]')
    driver.drag_and_drop(drag, drop)
    assert driver.css_element('div[id=column-a] header').text.lower() == 'b'

    driver.get(f'https://dineshvelhal.github.io/testautomation-playground/mouse_events.html')
    drag = driver.css_element('#drag_source')
    drop = driver.css_element('#drop_target')
    driver.drag_and_drop(drag, drop)
    assert "success" in drop.text.lower()
