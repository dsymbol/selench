import os
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from .browser import BrowserSetup


class Selench:
    def __init__(self, browser: str = "chrome", wait: int = 10, headless: bool = False,
                 incognito: bool = False):
        self.webdriver = BrowserSetup(browser, headless, incognito).create_driver()
        self.wait = wait

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, w):
        if w < 0:
            raise ValueError("Wait cannot be negative")
        self._wait = w

    @property
    def title(self):
        return self.webdriver.title

    @property
    def url(self):
        return self.webdriver.current_url

    @property
    def current_window_handle(self):
        return self.webdriver.current_window_handle

    @property
    def all_window_handles(self):
        return self.webdriver.window_handles

    def css_element(self, locator: str, timeout: int = None):
        if timeout:
            element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.CSS_SELECTOR, locator),
                                                                   f"Could not find element with the CSS `{locator}`")
        else:
            element = WebDriverWait(self.webdriver, self.wait).until(lambda d: d.find_element(By.CSS_SELECTOR, locator),
                                                                     f"Could not find element with the CSS `{locator}`")
        element.locator = (By.CSS_SELECTOR, locator)
        return element

    def css_elements(self, locator: str, timeout: int = None):
        try:
            if timeout:
                elements = WebDriverWait(self.webdriver, timeout).until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, locator),
                    f"Could not find elements with the CSS `{locator}`")
            else:
                elements = WebDriverWait(self.webdriver, self.wait).until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, locator),
                    f"Could not find elements with the CSS `{locator}`")
            for i in elements:
                i.locator = (By.CSS_SELECTOR, locator)
        except TimeoutException:
            elements = []
        return elements

    def xpath_element(self, locator: str, timeout: int = None):
        if timeout:
            element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.XPATH, locator),
                                                                   f"Could not find element with the XPATH `{locator}`")
        else:
            element = WebDriverWait(self.webdriver, self.wait).until(lambda d: d.find_element(By.XPATH, locator),
                                                                     f"Could not find element with the XPATH `{locator}`")
        element.locator = (By.XPATH, locator)
        return element

    def xpath_elements(self, locator: str, timeout: int = None):
        try:
            if timeout:
                elements = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_elements(By.XPATH, locator),
                                                                        f"Could not find elements with the XPATH `{locator}`")
            else:
                elements = WebDriverWait(self.webdriver, self.wait).until(lambda d: d.find_elements(By.XPATH, locator),
                                                                          f"Could not find elements with the XPATH `{locator}`")
            for i in elements:
                i.locator = (By.XPATH, locator)
        except TimeoutException:
            elements = []
        return elements

    @staticmethod
    def select_element(element: WebElement):
        """
        Select lists have special behaviors compared to other elements

        :Usage:
            element = driver.css_element('select')
            select_object = driver.select_element(element)

            # Select an <option> based upon the <select> element's internal index
            select_object.select_by_index(1)

            # Select an <option> based upon its value attribute
            select_object.select_by_value('value1')

            # Select an <option> based upon its text
            select_object.select_by_visible_text('Bread')
        """
        return Select(element)

    def hover(self, element: WebElement):
        """
        Hover over web element
        """
        ActionChains(self.webdriver).move_to_element(element).perform()

    def double_click(self, element: WebElement):
        """
        Double click web element
        """
        ActionChains(self.webdriver).double_click(element).perform()

    def right_click(self, element: WebElement):
        """
        Right click web element
        """
        ActionChains(self.webdriver).context_click(element).perform()

    def drag_and_drop(self, draggable: WebElement, droppable: WebElement, alternative=False):
        """
        If native selenium drag and drop don't work try the alternative method by passing alternative=True
        elements passed must be CSS elements.
        Credits: https://github.com/SeleniumHQ/selenium/issues/8003
        """
        if not alternative:
            ActionChains(self.webdriver).click_and_hold(draggable).move_to_element(droppable).perform()
            ActionChains(self.webdriver).release().perform()

        else:
            if draggable.locator[0] != 'css selector' or droppable.locator[0] != 'css selector':
                raise ValueError("Drag and drop only accepts elements found by CSS selectors")
            file_path = os.path.join(str(Path(os.path.abspath(__file__)).parents[0]), 'js', 'drag_and_drop.js')
            with open(file_path, "r") as f:
                javascript = f.read()
            self.execute_js(javascript, draggable, droppable)

    def wait_element_visibility(self, element: WebElement, timeout: int = None):
        """
        An expectation for checking that an element, known to be present on the DOM of a page, is visible. Visibility 
        means that the element is not only displayed but also has a height and width that is greater than 0. element 
        is the WebElement returns the (same) WebElement once it is visible 

        :Usage:
            element = driver.css_element('header')
            driver.wait_element_visibility(element)
        """
        if timeout:
            element = WebDriverWait(self.webdriver, timeout).until(ec.visibility_of(element), "Element is not visible")
        else:
            element = WebDriverWait(self.webdriver, self.wait).until(ec.visibility_of(element),
                                                                     "Element is not visible")
        return element

    def wait_element_staleness(self, element: WebElement, timeout: int = None):
        """
        Wait until an element is no longer attached to the DOM. element is the element to wait for.
        returns False if the element is still attached to the DOM, true otherwise.

        :Usage:
            element = driver.css_element('header')
            driver.wait_element_staleness(element)
        """
        if timeout:
            element = WebDriverWait(self.webdriver, timeout).until(ec.staleness_of(element),
                                                                   "Element did not go stale")
        else:
            element = WebDriverWait(self.webdriver, self.wait).until(ec.staleness_of(element),
                                                                     "Element did not go stale")
        return element

    def has_text(self, text: str):
        """
        ⚠️CASE SENSITIVE
        Looks for string anywhere on the page, returns a WebElements containing found text if element is visible.
        """
        elements = self.xpath_elements(f'//*[contains(text(),"{text}")]')
        found = []
        for i in elements:
            if text in i.text and i.is_displayed():
                found.append(i)
        return found

    def new_window(self):
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("window")
        WebDriverWait(self.webdriver, self.wait).until(ec.number_of_windows_to_be(expected_number),
                                                       "Number of windows is not equal to expected number "
                                                       f"`{expected_number}`")

    def new_tab(self):
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("tab")
        WebDriverWait(self.webdriver, self.wait).until(ec.number_of_windows_to_be(expected_number),
                                                       "Number of windows is not equal to expected number "
                                                       f"`{expected_number}`")

    def switch_window(self, name: str = None, index: int = None):
        if name:
            self.webdriver.switch_to.window(name)
        elif index >= 0:
            handle_name = self.all_window_handles[index]
            self.webdriver.switch_to.window(handle_name)

    def switch_frame(self, element: WebElement):
        """
        Switching using a WebElement is the most flexible option. You can find the frame using your preferred
        selector and switch to it.

        :Usage:
            # Using web element
            iframe = driver.css_element("iframe[id=ifr]")
            driver.switch_frame(iframe)
        """
        frame = WebDriverWait(self.webdriver, self.wait).until(
            ec.frame_to_be_available_and_switch_to_it(element.locator), "Frame is not available")
        return frame

    def parent_frame(self):
        """
        Switch to frame's frame parent
        """
        self.webdriver.switch_to.parent_frame()

    def leave_frame(self):
        """
        Exit all frames
        """
        self.webdriver.switch_to.default_content()

    def alert(self):
        """
        WebDriver provides an API for working with the native popup messages offered by JavaScript.
        These popups are styled by the browser and offer limited customisation.

        :Usage:
            alert = driver.alert()
            alert.accept()
            alert.dismiss()
            alert.send_keys('foo')
            alert.text
        """
        alert = WebDriverWait(self.webdriver, self.wait).until(ec.alert_is_present(), "No alerts are present")
        return alert

    def basic_auth(self, url, username, password):
        """
        Basic javascript username:password url authentication
        """
        new_url = url.replace('//', f'//{username}:{password}@')
        self.get(new_url)

    def get(self, url: str):
        self.webdriver.get(url)

    def refresh(self):
        self.webdriver.refresh()

    def close(self):
        self.webdriver.close()

    def delete_cookies(self):
        self.webdriver.delete_all_cookies()

    def screenshot(self, filename: str):
        self.webdriver.save_screenshot(filename)

    def forward(self):
        self.webdriver.forward()

    def back(self):
        self.webdriver.back()

    def execute_js(self, js: str, *args):
        """
        Executes JavaScript in the current window/frame

        :Usage:
            title = driver.execute_js('return document.title;')
            driver.execute_js('document.getElementsByClassName("viewcode-link")[0].click()')
        """
        return self.webdriver.execute_script(js, *args)

    def maximize(self):
        self.webdriver.maximize_window()

    def minimize(self):
        self.webdriver.minimize_window()

    def set_window_position(self, x: int, y: int, window_handle: str = None):
        self.webdriver.set_window_position(x, y, windowHandle=window_handle)

    def get_window_position(self, window_handle: str = None):
        return self.webdriver.get_window_position(windowHandle=window_handle)

    def get_window_size(self, window_handle: str = None):
        return self.webdriver.get_window_size(windowHandle=window_handle)

    def set_window_size(self, width: int, height: int, window_handle: str = None):
        self.webdriver.set_window_size(width, height, windowHandle=window_handle)

    def get_window_geometry(self):
        return self.webdriver.get_window_rect()

    def quit(self):
        self.webdriver.quit()
