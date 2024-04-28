import shared


def test_hover(driver):
    driver.get(f'{shared.CBT}/hover-menu.html')
    driver.element('//li[@class="dropdown"] /a').hover()
    new_visible_elements = driver.elements('//ul[@class="dropdown-menu"] //li /a[not(@onclick)]')
    assert all([i.is_displayed for i in new_visible_elements])


def test_double_click(driver):
    driver.get('https://www.javatpoint.com/oprweb/test.jsp?filename=javascript-dblclick-event1')
    driver.switch_frame('//iframe[@id="iframewrapper"]')
    driver.element('//*[@id="heading"]').double_click()
    assert "javatpoint.com" in driver.element('//*[@id="heading"]').text.lower()


def test_right_click(driver):
    driver.get(f'{shared.INTERNET}/context_menu')
    driver.element('div[id=hot-spot]').right_click()
    alert = driver.alert()
    assert alert.text.lower() == 'you selected a context menu'


def test_drag_and_drop(driver):
    expected = 'Dropped!'
    driver.get(f'{shared.CBT}/drag-and-drop.html')
    drag = driver.element('#draggable')
    drop = driver.element('#droppable')
    drag.drag_to(drop)
    driver.expect.element_text_to_be('div[id=droppable] p', expected)
    assert driver.element('div[id=droppable] p').text == expected

    driver.get(f'{shared.INTERNET}/drag_and_drop')
    drag = driver.element('div[id=column-a]')
    drop = driver.element('div[id=column-b]')
    drag.drag_to(drop)
    assert driver.element('div[id=column-a] header').text.lower() == 'b'

    driver.get(f'https://dineshvelhal.github.io/testautomation-playground/mouse_events.html')
    drag = driver.element('#drag_source')
    drop = driver.element('#drop_target')
    drag.drag_to(drop)
    assert "success" in drop.text.lower()
