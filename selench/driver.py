"""
Main module that holds all the methods to interact with the browser.

::

    from selench import Selench, Keys

    driver = Selench()
    driver.get('https://google.com')
    driver.element('input[name="q"]').send_keys('Hello World!', Keys.ENTER)
    driver.quit()
"""

import json
from contextlib import contextmanager
from pathlib import Path
from typing import List, Literal

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from .element import Element
from .expect import Expect


class Selench:
    """
    This is the main class that holds all the methods to interact with the browser.

    Args:
        driver: WebDriver instance used to interact with the browser.
        timeout: The default explicit timeout for WebDriverWait.
    """

    def __init__(
        self,
        driver: WebDriver | Literal["Chrome", "Firefox", "Edge"] = "Chrome",
        timeout: int = 10,
    ) -> None:
        self.webdriver = driver
        self.wait = timeout
        self._expect = Expect(self)

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

    @webdriver.setter
    def webdriver(self, d):
        if isinstance(d, WebDriver):
            self._webdriver = d
        elif isinstance(d, str):
            if d.lower() == "chrome":
                self._webdriver = webdriver.Chrome()
            elif d.lower() == "firefox":
                self._webdriver = webdriver.Firefox()
            elif d.lower() == "edge":
                self._webdriver = webdriver.Edge()
            else:
                raise Exception("Unknown browser passed as WebDriver object")
        else:
            raise Exception("Unknown type passed to driver")

    @property
    def expect(self) -> Expect:
        """
        This property provides access to the Expect class, which contains explicit wait functions.

        Example::

            driver.expect.element_to_be_visible('input')
        """
        return self._expect

    def element(self, selector: str) -> Element:
        """
        Identifies the type of the provided selector and find the first matching element.

        Args:
            selector: The selector for the element.

        Returns:
            The found Element.

        Raises:
            Exception: If the element is not found.

        Example::

            # Would detect that #content is a CSS selector and return a CSS element
            element = driver.element('#content')

            # Would detect that //div is not a CSS selector and return an XPath element
            element = driver.element('//div')
        """
        locator = self._detect_selector(selector)
        element = self.wait.until(
            lambda d: d.find_element(*locator),
            f"Could not find element with the {locator}",
        )
        return Element(self, element, locator)

    def elements(self, selector: str) -> List[Element]:
        """
        Identifies the type of the provided selector and find a list of matching element.

        Args:
            selector: The selector for the elements.

        Returns:
            A list of the found Elements. If no elements are found, an empty list is returned.

        Example::

            # Would detect that #content is a CSS selector and return a list of CSS elements
            elements = driver.elements('#content')

            # Would detect that //div is not a CSS selector and return a list of XPath elements
            elements = driver.elements('//div')
        """
        try:
            locator = self._detect_selector(selector)
            elements = self.wait.until(
                lambda d: d.find_elements(*locator),
                f"Could not find elements with the {locator}",
            )
            elements = [Element(self, element, locator) for element in elements]
        except TimeoutException:
            elements = []
        return elements

    @property
    def wait(self) -> WebDriverWait:
        """
        The default explicit wait time for WebDriverWait.

        Returns:
            int: Wait time
        """
        return self._wait

    @wait.setter
    def wait(self, w: int):
        if w < 0:
            raise ValueError("Wait cannot be negative")
        self._wait = WebDriverWait(self.webdriver, w)

    @contextmanager
    def temp_wait(self, timeout: int) -> None:
        """
        Temporarily change WebDriverWait timeout.

        Args:
            timeout: Temporary wait time for WebDriverWait.

        Example::

            with driver.temp_wait(20):
                driver.element("#desc")
        """
        old_wait = self.wait._timeout
        self.wait = timeout
        yield
        self.wait = old_wait

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

    def _detect_selector(self, selector: str) -> tuple[str, str]:
        """
        Detects if a selector is CSS. Returns (By.CSS_SELECTOR, selector) if it is, else (By.XPATH, selector).
        """
        js = """
        const queryCheck = (s) => document.createDocumentFragment().querySelector(s)

        const isSelectorValid = (selector) => {
          try { queryCheck(selector) } catch { return false }
          return true
        }    

        return isSelectorValid(arguments[0])
        """
        return (
            (By.CSS_SELECTOR, selector)
            if self.execute_js(js, selector)
            else (By.XPATH, selector)
        )

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
        self.execute_js("window.scrollTo(0, document.body.scrollHeight)")

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
        return self.webdriver.get_log(log_type)

    def new_window(self) -> None:
        """
        Open a new browser window.
        """
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("window")
        self.wait.until(
            ec.number_of_windows_to_be(expected_number),
            "Number of windows is not equal to expected number " f"`{expected_number}`",
        )

    def new_tab(self) -> None:
        """
        Open a new browser tab.
        """
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("tab")
        self.wait.until(
            ec.number_of_windows_to_be(expected_number),
            "Number of windows is not equal to expected number " f"`{expected_number}`",
        )

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

    def switch_frame(self, selector: str) -> bool:
        """
        Switch the focus of future commands to the frame identified by its selector.

        Args:
            selector: The selector for the frame.

        Returns:
            True if the frame was found and switched to

        Raises:
            Exception: If the frame is not found.

        Example::
            driver.switch_frame("iframe[id=ifr]")
        """
        locator = self._detect_selector(selector)
        frame = self.wait.until(
            ec.frame_to_be_available_and_switch_to_it(locator), "Frame is not available"
        )
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

    def alert(self) -> Alert:
        """
        Get the alert box that is currently open.

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
        alert = self.wait.until(ec.alert_is_present(), "No alerts are present")
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
        new_url = url.replace("//", f"//{username}:{password}@")
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

    def session(self, path: str = "cookies.json", prompt=False) -> None:
        """
        Save and load session cookies to and from a specified file path.
        If file path doesn't exist, it saves the current session cookies to the specified path.
        Otherwise, it loads the session cookies from the specified path.

        Args:
            path (str): The file path to save or load the session cookies from. Default is "cookies.pkl"
            prompt (bool): Prompts the user to press enter before saving session cookies. Default is False
        """
        path = Path(path).absolute()

        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                cookies = json.load(f)
            [self.add_cookie(cookie) for cookie in cookies]
            self.refresh()
        else:
            if prompt:
                input("Press ENTER once ready to save the session")
            cookies = self.get_all_cookies()
            with path.open("w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=4)

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

    def set_page_load_timeout(self, time: float) -> None:
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

    def set_window_size(
        self, width: int, height: int, window_handle: str = None
    ) -> None:
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
