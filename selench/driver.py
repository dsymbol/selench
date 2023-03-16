"""
Main module that holds all the methods to interact with the browser.

::

    from selench import Selench, Keys

    driver = Selench()
    driver.get('https://google.com')
    driver.element('input[name="q"]').send_keys('Hello World!', Keys.ENTER)
    driver.quit()
"""

import os
import pickle
from typing import List, Literal, Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from .browser import Browser
from .wait_for import WaitFor


class Selench:
    """
    This is the main class that holds all the methods to interact with the browser.

    Args:
        browser: The browser to use.
        wait: The default explicit wait time for WebDriverWait.
        executable_path: The path to the driver executable.
        headless: Run browser in headless mode.
        user_agent: The user agent to use.
        incognito: Run browser in incognito mode.
        binary_location: The location of the browser executable.
    """

    def __init__(
            self,
            browser: Literal["chrome", "firefox"] = "chrome",
            wait: int = 10,
            executable_path: str = None,
            headless: bool = False,
            user_agent: str = None,
            incognito: bool = False,
            binary_location: str = None
    ):
        self._webdriver = Browser(browser, executable_path, headless, user_agent, incognito,
                                  binary_location).create_driver()
        self.wait = wait
        self._wait_for = WaitFor(self)

    @property
    def webdriver(self):
        """
        This property provides access to the underlying webdriver instance.
        Can be used to access webdriver's methods and properties that are not yet implemented in this package.

        Returns:
            webdriver instance

        Example::

            driver.webdriver.get("https://www.google.com")
        """
        return self._webdriver

    @property
    def wait_for(self) -> WaitFor:
        """
        This property provides access to the WaitFor class, which contains explicit wait functions.

        Example::

            driver.wait_for.element_visibility('input')
        """
        return self._wait_for

    def css_element(self, selector: str, timeout: int = None) -> WebElement:
        """
        Find the first matching element on a page by its CSS selector.

        Args:
            selector: The CSS selector for the element.
            timeout: The time to wait for the element to be found. Default is None, which means use the default wait time.

        Returns:
            The found WebElement.

        Raises:
            Exception: If the element is not found.

        Example::

            element = driver.css_element('#content')
        """
        if not timeout: timeout = self.wait
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.CSS_SELECTOR, selector),
                                                               f"Could not find element with the CSS `{selector}`")
        return element

    def css_elements(self, selector: str, timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements on the page by their CSS selector.

        Args:
            selector: The CSS selector for the elements.
            timeout: The time to wait for the elements to be found. Default is None, which means use the default wait time.

        Returns:
            A list of the found WebElements. If no elements are found, an empty list is returned.

        Example::

            elements = driver.css_elements('#content')
        """
        if not timeout: timeout = self.wait
        try:
            elements = WebDriverWait(self.webdriver, timeout).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, selector),
                f"Could not find elements with the CSS `{selector}`")
        except TimeoutException:
            elements = []
        return elements

    def xpath_element(self, selector: str, timeout: int = None) -> WebElement:
        """
        Find the first matching element on a page by its XPATH selector.

        Args:
            selector: The XPATH selector for the element.
            timeout: The time to wait for the element to be found. Default is None, which means use the default wait time.

        Returns:
            The found WebElement.

        Raises:
            Exception: If the element is not found.

        Example::

            element = driver.xpath_element('//div')
        """
        if not timeout: timeout = self.wait
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.XPATH, selector),
                                                               f"Could not find element with the XPATH `{selector}`")
        return element

    def xpath_elements(self, selector: str, timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements on the page by their XPATH selector.

        Args:
            selector: The XPATH selector for the elements.
            timeout: The time to wait for the elements to be found. Default is None, which means use the default wait time.

        Returns:
            A list of the found WebElements. If no elements are found, an empty list is returned.

        Example::

            elements = driver.xpath_elements('//div')
        """
        try:
            if not timeout: timeout = self.wait
            elements = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_elements(By.XPATH, selector),
                                                                    f"Could not find elements with the XPATH `{selector}`")
        except TimeoutException:
            elements = []
        return elements

    def element(self, selector: str, timeout: int = None) -> WebElement:
        """
        Identifies the type of the provided selector and find the first matching element.

        Args:
            selector: The selector for the element.
            timeout: The time to wait for the element to be found. Default is None, which means use the default wait time.

        Returns:
            The found WebElement.

        Raises:
            Exception: If the element is not found.

        Example::

            # Would detect that #content is a CSS selector and return a CSS element
            element = driver.element('#content')

            # Would detect that //div is not a CSS selector and return an XPath element
            element = driver.element('//div')
        """
        if not timeout: timeout = self.wait
        locator = self._detect_locator_type(selector)
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(*locator),
                                                               f"Could not find element with the {locator}")
        return element

    def elements(self, selector: str, timeout: int = None) -> List[WebElement]:
        """
        Identifies the type of the provided selector and find a list of matching element.

        Args:
            selector: The selector for the element.
            timeout: The time to wait for the elements to be found. Default is None, which means use the default wait time.

        Returns:
            A list of the found WebElements. If no elements are found, an empty list is returned.

        Example::

            # Would detect that #content is a CSS selector and return a list of CSS elements
            elements = driver.elements('#content')

            # Would detect that //div is not a CSS selector and return a list of XPath elements
            elements = driver.elements('//div')
        """
        try:
            if not timeout: timeout = self.wait
            locator = self._detect_locator_type(selector)
            elements = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_elements(*locator),
                                                                    f"Could not find elements with the {locator}")
        except TimeoutException:
            elements = []
        return elements

    def click(self, selector: str, timeout: int = None) -> None:
        """
        Clicks on an element on the webpage using the given selector.
        Waits for the element to be clickable before clicking.

        Args:
            selector: selector of the element to be clicked
            timeout: maximum time to wait for the element to be clicked. Default is None, which means use the default wait time.

        Example::

            driver.click('#button')
        """
        if not timeout: timeout = self.wait
        self.wait_for.element_clickable(selector, timeout).click()

    def send_keys(self, selector: str, *values, timeout: int = None) -> None:
        """
        Sends keys to an element on the webpage using the given selector.
        Waits for the element to be visible and enabled before sending keys.

        Args:
            selector: selector of the element to send keys to
            *values: keys to be sent to the element
            timeout: maximum time to wait for the keys to be sent. Default is None, which means use the default wait time.

        Example::

            from selench import Keys

            driver.send_keys('textarea', 'Hello World', Keys.ENTER)
        """
        if not timeout: timeout = self.wait
        self.wait_for.element_clickable(selector, timeout).send_keys(*values)

    @property
    def wait(self) -> int:
        """
        The default explicit wait time for WebDriverWait.

        Returns:
            int: Wait time
        """
        return self._wait

    @wait.setter
    def wait(self, w):
        if w < 0:
            raise ValueError("Wait cannot be negative")
        self._wait = w

    @property
    def title(self) -> str:
        """
        Returns the title of the current page.
        """
        return self.webdriver.title

    @property
    def url(self) -> str:
        """
        Returns the url of the current page.
        """
        return self.webdriver.current_url

    @property
    def user_agent(self) -> str:
        """
        Returns the user agent of the current browser instance.
        """
        user_agent = self.execute_js("return navigator.userAgent;")
        return user_agent

    @property
    def browser(self) -> str:
        """
        Returns the name of the browser instance.
        """
        return self.webdriver.name

    @property
    def current_window_handle(self) -> str:
        """
        Returns the handle of the current window.
        """
        return self.webdriver.current_window_handle

    @property
    def all_window_handles(self) -> List[str]:
        """
        Returns a list of all window handles.
        """
        return self.webdriver.window_handles

    @property
    def log_types(self) -> List[str]:
        """
        Returns a list of log types available to the webdriver.
        """
        return self.webdriver.log_types

    def _detect_locator_type(self, selector: str):
        """
        Detects if selector is CSS and returns a CSS locator otherwise returns a XPath locator
        """
        if self._is_css(selector):
            locator = (By.CSS_SELECTOR, selector)
        else:
            locator = (By.XPATH, selector)
        return locator

    def _is_css(self, selector: str) -> bool:
        script = """
        const queryCheck = (s) => document.createDocumentFragment().querySelector(s)
        
        const isSelectorValid = (selector) => {
          try { queryCheck(selector) } catch { return false }
          return true
        }    
        
        return isSelectorValid(arguments[0])
        """
        return self.execute_js(script, selector)

    def clear(self, selector: str, timeout: int = None) -> None:
        """
        Clears the text of an element on the webpage using the given selector.
        Waits for the element to be visible and enabled before clearing.

        Args:
            selector: selector of the element to be cleared
            timeout: maximum time to wait for the element to be cleared. Default is None, which means use the default wait time.
        """
        if not timeout: timeout = self.wait
        self.wait_for.element_clickable(selector, timeout).clear()

    def hover(self, element: WebElement):
        """
        Move the mouse cursor over the provided web element.

        Args:
            element: The web element to hover over.
        """
        ActionChains(self.webdriver).move_to_element(element).perform()

    def double_click(self, element: WebElement):
        """
        Perform a double click on the provided web element.

        Args:
            element: The web element to perform the double click on.
        """
        ActionChains(self.webdriver).double_click(element).perform()

    def right_click(self, element: WebElement):
        """
        Perform a right click on the provided web element.

        Args:
            element: The web element to perform the right click on.
        """
        ActionChains(self.webdriver).context_click(element).perform()

    def scroll_to_element(self, element: WebElement):
        """
        Scroll the page to the provided web element.

        Args:
            element: The web element to scroll to.
        """
        ActionChains(self.webdriver).scroll_to_element(element).perform()

    def scroll_amount(self, x: int, y: int):
        """
        Scroll the page by a specified amount in the x and y directions.

        Args:
            x: The amount to scroll in the horizontal direction. Negative values scroll left, positive values scroll right.
            y: The amount to scroll in the vertical direction. Negative values scroll up, positive values scroll down.
        """
        ActionChains(self.webdriver).scroll_by_amount(x, y).perform()

    def scroll_to_page_bottom(self):
        """
        Scroll the page to the bottom.
        """
        self.driver.execute_js('window.scrollTo(0, document.body.scrollHeight)')

    def drag_and_drop(self, draggable: WebElement, droppable: WebElement, alternative=False):
        """
        Perform a drag and drop action on the provided web elements.

        Args:
            draggable: The web element to be dragged.
            droppable: The web element to be dropped on.
            alternative: Whether to use an alternative method for the drag and drop action. Default is False.
        """
        if not alternative:
            ActionChains(self.webdriver).click_and_hold(draggable).move_to_element(droppable).perform()
            ActionChains(self.webdriver).release().perform()
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'js', 'drag_and_drop.js')
            with open(file_path, "r") as f:
                javascript = f.read()
            self.driver.execute_js(javascript, draggable, droppable)

    def select_element(self, element_or_selector: Union[str, WebElement]) -> Select:
        """
        Convert a web element to a Select object. The Select object provides a convenient way to interact with
        select elements (drop-down lists) on a webpage. It allows the user to select one or more options from the list,
        and also provides methods to retrieve the selected options, as well as other useful information about the select element.

        Args:
            element_or_selector: The web element or selector to convert to a Select object.

        Returns:
            Select: The converted Select object.

        Example::

            element = driver.css_element('select')
            select_object = driver.select_element(element)

            # Select an <option> based upon the <select> element's internal index
            select_object.select_by_index(1)

            # Select an <option> based upon its value attribute
            select_object.select_by_value('value1')

            # Select an <option> based upon its text
            select_object.select_by_visible_text('Bread')
        """
        if isinstance(element_or_selector, str):
            element_or_selector = self.element(element_or_selector)
        elif isinstance(element_or_selector, WebElement):
            pass
        else:
            raise ValueError('Unsupported variable type ' + str(type(element_or_selector)))
        return Select(element_or_selector)

    def execute_js(self, script: str, *args):
        """
        Execute a JavaScript script on the current page.

        Args:
            script: The JavaScript script to execute.
            *args: Any additional arguments to pass to the script.

        Returns:
            The return value of the script, if any.

        Example::

            # get title of current page
            title = driver.execute_js('return document.title;')
            # click an element with an id of content
            driver.execute_js('document.querySelector('#content').click()')
        """
        return self.webdriver.execute_script(script, *args)

    def get_page_source(self) -> str:
        """
        Get the entire HTML source of the current page.

        Returns:
            The HTML source of the current page.
        """
        return self.webdriver.page_source

    def get_log(self, log_type: str):
        """
        Get the log for a specific log type.

        Args:
            log_type: The type of log to retrieve. Use the log_types attribute to get a list of available log types.

        Returns:
            A list of log entries for the specified log type.
        """
        self.webdriver.get_log(log_type)

    def new_window(self, timeout: int = None) -> None:
        """
        Open a new browser window.

        Args:
            timeout: The time to wait for the new window to open. Default is None, which means use the default wait time.
        """
        if not timeout: timeout = self.wait
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("window")
        WebDriverWait(self.webdriver, timeout).until(ec.number_of_windows_to_be(expected_number),
                                                     "Number of windows is not equal to expected number "
                                                     f"`{expected_number}`")

    def new_tab(self, timeout: int = None) -> None:
        """
        Open a new browser tab.

        Args:
            timeout: The time to wait for the new tab to open. Default is None, which means use the default wait time.
        """
        if not timeout: timeout = self.wait
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("tab")
        WebDriverWait(self.webdriver, timeout).until(ec.number_of_windows_to_be(expected_number),
                                                     "Number of windows is not equal to expected number "
                                                     f"`{expected_number}`")

    def switch_window(self, name: str = None, index: int = None) -> None:
        """
        Switch focus to a different browser window or tab.

        Args:
            name: The name of the window or tab to switch to.
            index: The index of the window or tab to switch to.
        """
        if name:
            self.webdriver.switch_to.window(name)
        elif index >= 0:
            handle_name = self.all_window_handles[index]
            self.webdriver.switch_to.window(handle_name)

    def switch_frame(self, selector: str, timeout: int = None) -> bool:
        """
        Switch the focus of future commands to the frame identified by its selector.

        Args:
            selector: The selector for the frame.
            timeout: The time to wait for the frame to be available. Default is None, which means use the default wait time.

        Returns:
            True if the frame was found and switched to

        Raises:
            Exception: If the frame is not found.

        Example::
            driver.switch_frame("iframe[id=ifr]")
        """
        if not timeout: timeout = self.wait
        locator = self._detect_locator_type(selector)
        frame = WebDriverWait(self.webdriver, timeout).until(ec.frame_to_be_available_and_switch_to_it(locator),
                                                             "Frame is not available")
        return frame

    def parent_frame(self) -> None:
        """
        Switch to the parent frame of the current frame.
        """
        self.webdriver.switch_to.parent_frame()

    def leave_frame(self) -> None:
        """
        Exit all frames and switch to the default content.
        """
        self.webdriver.switch_to.default_content()

    def alert(self, timeout: int = None) -> Alert:
        """
        Get the alert box that is currently open.

        Args:
            timeout: The time to wait for the alert to appear. Default is None, which means use the default wait time.

        Returns:
            The alert box that is currently open.

        Raises:
            TimeoutException: If the alert is not present within the specified timeout.

        Example::

            alert = driver.alert()
            alert.accept()
            alert.dismiss()
            alert.send_keys('foo')
            print(alert.text)
        """
        if not timeout: timeout = self.wait
        alert = WebDriverWait(self.webdriver, timeout).until(ec.alert_is_present(), "No alerts are present")
        return alert

    def basic_auth(self, url: str, username: str, password: str) -> None:
        """
        Perform basic URL authentication.

        Args:
            url: The URL to access, must include protocol (e.g. https://)
            username: The username for the authentication.
            password: The password for the authentication.

        Example::

            driver.basic_auth("https://example.com", "username", "password")
        """
        new_url = url.replace('//', f'//{username}:{password}@')
        self.get(new_url)

    def get(self, url: str) -> None:
        """
        Navigates to the specified URL.

        Args:
            url: The URL to navigate to.
        """
        self.webdriver.get(url)

    def refresh(self) -> None:
        """
        Refresh the current page.
        """
        self.webdriver.refresh()

    def close(self) -> None:
        """
        Closes the current window.
        """
        self.webdriver.close()

    def get_all_cookies(self) -> List[dict]:
        """
        Get all cookies of the current session.

        Returns:
            A list of dictionaries, with each dictionary representing a cookie.
        """
        return self.webdriver.get_cookies()

    def add_cookie(self, cookie_dict: dict) -> None:
        """
        Add a cookie to the current session.

        Args:
            cookie_dict: A dictionary representing the cookie, with keys "name" and "value".

        Example::

            driver.add_cookie({"name" : "foo", "value" : "bar"})
        """
        self.webdriver.add_cookie(cookie_dict)

    def delete_cookie(self, name: str) -> None:
        """
        Delete a specific cookie by name.

        Args:
            name: The name of the cookie to be deleted.

        Example::

            driver.delete_cookie("foo")
        """
        self.webdriver.delete_cookie(name)

    def delete_all_cookies(self) -> None:
        """
        Delete all cookies for the current session.
        """
        self.webdriver.delete_all_cookies()

    def session(self, path: str = "cookies.pkl", prompt=False) -> None:
        """
        Save and load session cookies to and from a specified file path.
        If file path doesn't exist, it saves the current session cookies to the specified path.
        Otherwise, it loads the session cookies from the specified path.

        Args:
            path (str): The file path to save or load the session cookies from. Default is "cookies.pkl"
            prompt (bool): Prompts the user to press enter before saving session cookies. Default is False
        """
        if os.path.exists(path):
            with open(path, "rb") as f:
                cookies = pickle.load(f)
            [self.add_cookie(cookie) for cookie in cookies]
            self.refresh()
        else:
            if prompt:
                input("Press ENTER once ready to save the session")
            cookies = self.get_all_cookies()
            with open(path, "wb") as f:
                pickle.dump(cookies, f)

    def screenshot(self, path: str = "screenshot.png") -> bool:
        """
        Saves a screenshot of the current window to a PNG image file.

        Args:
            path: The file path to save the screenshot. Default is "screenshot.png"

        Returns:
            Returns False if there is any IOError, else returns True.
        """
        return self.webdriver.save_screenshot(path)

    def forward(self) -> None:
        """
        Goes forward in browser history.
        """
        self.webdriver.forward()

    def back(self) -> None:
        """
        Goes back in browser history.
        """
        self.webdriver.back()

    def maximize(self) -> None:
        """
        Maximize the current window.
        """
        self.webdriver.maximize_window()

    def minimize(self) -> None:
        """
        Minimize the current window.
        """
        self.webdriver.minimize_window()

    def fullscreen(self) -> None:
        """
        Make the current window fullscreen.
        """
        self.webdriver.fullscreen_window()

    def set_page_load_timeout(self, time: Union[int, float]) -> None:
        """
        Set the timeout for page load.

        Args:
            time: timeout in seconds
        """
        self.webdriver.set_page_load_timeout(time)

    def set_window_position(self, x: int, y: int, window_handle: str = None) -> dict:
        """
        Set the position of the current window.

        Args:
            x: The x position of the window
            y: The y position of the window
            window_handle: The window handle to set the position of. If None, set the position of the current window.

        Returns:
            dict : containing x and y position of the window
        """
        return self.webdriver.set_window_position(x, y, windowHandle=window_handle)

    def get_window_position(self, window_handle: str = None) -> dict:
        """
        Get the position of the current window.

        Args:
            window_handle: The window handle to get the position of. If None, get the position of the current window.

        Returns:
            dict : containing x and y position of the window
        """
        return self.webdriver.get_window_position(windowHandle=window_handle)

    def get_window_size(self, window_handle: str = None) -> dict:
        """
         Get the size of the browser window.

        Args:
            window_handle:The window handle to get the size of. If None, get the size of the current window.

        Returns:
            A dictionary containing the width and height of the browser window.
        """
        return self.webdriver.get_window_size(windowHandle=window_handle)

    def set_window_size(self, width: int, height: int, window_handle: str = None) -> None:
        """
        Set the size of a browser window.

        Args:
            width: The width of the browser window.
            height: The height of the browser window.
            window_handle:The window handle to set the size of. If None, sets the size of the current window.
        """
        self.webdriver.set_window_size(width, height, windowHandle=window_handle)

    def get_window_geometry(self) -> dict:
        """
        Get the geometry of the browser window.

        Returns:
            A dictionary containing the x, y, width and height of the browser window.
        """
        return self.webdriver.get_window_rect()

    def quit(self) -> None:
        """
        Close all windows and quit the browser.
        """
        self.webdriver.quit()
