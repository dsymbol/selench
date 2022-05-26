crossbrowsertesting = "https://crossbrowsertesting.github.io"


def test_select_element(driver):
    driver.get(f'{crossbrowsertesting}/selenium_example_page.html')
    select_element = driver.css_element('#dropdown')
    sel = driver.select_element(select_element)
    sel.select_by_value('option2')
    assert driver.css_element('option[value=option2]').is_selected()
    sel.select_by_index(2)
    assert driver.css_element('option[value=option3]').is_selected()


def test_hover(driver):
    driver.get(f'{crossbrowsertesting}/hover-menu.html')
    dd_element = driver.xpath_element('//li[@class="dropdown"] /a')
    driver.hover(dd_element)
    new_visable_elements = driver.xpath_elements('//ul[@class="dropdown-menu"] //li /a[not(@onclick)]')
    assert all([i.is_displayed for i in new_visable_elements])


def test_double_click(driver):
    driver.get('https://www.javatpoint.com/oprweb/test.jsp?filename=javascript-dblclick-event1')
    frame = driver.xpath_element('//iframe[@id="iframewrapper"]')
    driver.switch_frame(frame)
    dbl_element = driver.xpath_element('//*[@id="heading"]')
    driver.double_click(dbl_element)
    driver.wait_element_staleness(dbl_element)
    dbl_element = driver.xpath_element('//*[@id="heading"]')
    assert "javatpoint.com" in dbl_element.text.lower()


def test_right_click(driver):
    driver.get('https://the-internet.herokuapp.com/context_menu')
    rclick_element = driver.css_element('div[id=hot-spot]')
    driver.right_click(rclick_element)
    alert = driver.alert()
    assert alert.text.lower() == 'you selected a context menu'


def test_drag_and_drop(driver):
    expected = 'Dropped!'
    driver.get(f'{crossbrowsertesting}/drag-and-drop.html')
    drag = driver.css_element('div[id=draggable]')
    drop = driver.css_element('div[id=droppable]')
    driver.drag_and_drop(drag, drop)
    driver.wait_element_text(drop, expected)
    assert driver.css_element('div[id=droppable] p').text == expected
