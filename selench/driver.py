import os
import pickle
from typing import List, Literal, Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from .action import Action
from .browser import Browser
from .wait_for import WaitFor


class Selench:
    def __init__(
            self,
            browser: Literal["chrome", "firefox"] = "chrome",
            wait: int = 10,
            executable_path: str = None,
            headless: bool = False,
            user_agent: str = None,
            incognito: bool = False):
        self.webdriver = Browser(browser, executable_path, headless, user_agent, incognito).create_driver()
        self.wait = wait
        self._wait_for = WaitFor(self)
        self._action = Action(self)

    @property
    def wait(self) -> int:
        return self._wait

    @wait.setter
    def wait(self, w):
        if w < 0:
            raise ValueError("Wait cannot be negative")
        self._wait = w

    @property
    def wait_for(self) -> WaitFor:
        return self._wait_for

    @property
    def action(self) -> Action:
        return self._action

    @property
    def title(self) -> str:
        return self.webdriver.title

    @property
    def url(self) -> str:
        return self.webdriver.current_url

    @property
    def user_agent(self) -> str:
        user_agent = self.execute_js("return navigator.userAgent;")
        return user_agent

    @property
    def browser(self) -> str:
        return self.webdriver.name

    @property
    def current_window_handle(self) -> str:
        return self.webdriver.current_window_handle

    @property
    def all_window_handles(self) -> List[str]:
        return self.webdriver.window_handles

    @property
    def log_types(self) -> List[str]:
        return self.webdriver.log_types

    def css_element(self, path: str, timeout: int = None) -> WebElement:
        if not timeout: timeout = self.wait
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.CSS_SELECTOR, path),
                                                               f"Could not find element with the CSS `{path}`")
        return element

    def css_elements(self, path: str, timeout: int = None) -> List[WebElement]:
        if not timeout: timeout = self.wait
        try:
            elements = WebDriverWait(self.webdriver, timeout).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, path),
                f"Could not find elements with the CSS `{path}`")
        except TimeoutException:
            elements = []
        return elements

    def xpath_element(self, path: str, timeout: int = None) -> WebElement:
        if not timeout: timeout = self.wait
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(By.XPATH, path),
                                                               f"Could not find element with the XPATH `{path}`")
        return element

    def xpath_elements(self, path: str, timeout: int = None) -> List[WebElement]:
        try:
            if not timeout: timeout = self.wait
            elements = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_elements(By.XPATH, path),
                                                                    f"Could not find elements with the XPATH `{path}`")
        except TimeoutException:
            elements = []
        return elements

    def element(self, path: str, timeout: int = None) -> WebElement:
        """
        Detects if path is CSS and returns a CSS element otherwise returns a XPath element

        :Usage:
            element = driver.element('#content')
            Would detect that #content is a CSS path and return a CSS element

            element = driver.element('//div')
            Would detect that //div is not a CSS path and return a XPath element
        """
        if not timeout: timeout = self.wait
        locator = self._detect_locator_type(path)
        element = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_element(*locator),
                                                               f"Could not find element with the {locator}")
        return element

    def elements(self, path: str, timeout: int = None) -> List[WebElement]:
        """
        Detects if path is CSS and returns CSS elements otherwise returns XPath elements

        :Usage:
            element = driver.element('#content')
            Would detect that #content is a CSS path and return CSS elements

            element = driver.element('//div')
            Would detect that //div is a XPath path and return XPath elements
        """
        try:
            if not timeout: timeout = self.wait
            locator = self._detect_locator_type(path)
            elements = WebDriverWait(self.webdriver, timeout).until(lambda d: d.find_elements(*locator),
                                                                    f"Could not find elements with the {locator}")
        except TimeoutException:
            elements = []
        return elements

    def _detect_locator_type(self, path: str):
        """
        Detects if path is CSS and returns a CSS locator otherwise returns a XPath locator
        """
        if self._is_css(path):
            locator = (By.CSS_SELECTOR, path)
        else:
            locator = (By.XPATH, path)
        return locator

    def _is_css(self, path: str) -> bool:
        script = """
        const queryCheck = (s) => document.createDocumentFragment().querySelector(s)
        
        const isSelectorValid = (selector) => {
          try { queryCheck(selector) } catch { return false }
          return true
        }    
        
        return isSelectorValid(arguments[0])
        """
        return self.execute_js(script, path)

    @staticmethod
    def select_element(element: WebElement) -> Select:
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

    def execute_js(self, js: str, *args):
        """
        Executes JavaScript in the current window/frame

        :Usage:
            title = driver.execute_js('return document.title;')
            driver.execute_js('document.getElementsByClassName("viewcode-link")[0].click()')
        """
        return self.webdriver.execute_script(js, *args)

    def get_page_source(self):
        return self.webdriver.page_source

    def get_log(self, log_type: str):
        """
        Gets the log for a given log type
        driver.log_types to get available log types
        """
        self.webdriver.get_log(log_type)

    def new_window(self, timeout: int = None):
        if not timeout: timeout = self.wait
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("window")
        WebDriverWait(self.webdriver, timeout).until(ec.number_of_windows_to_be(expected_number),
                                                     "Number of windows is not equal to expected number "
                                                     f"`{expected_number}`")

    def new_tab(self, timeout: int = None):
        if not timeout: timeout = self.wait
        expected_number = len(self.all_window_handles) + 1
        self.webdriver.switch_to.new_window("tab")
        WebDriverWait(self.webdriver, timeout).until(ec.number_of_windows_to_be(expected_number),
                                                     "Number of windows is not equal to expected number "
                                                     f"`{expected_number}`")

    def switch_window(self, name: str = None, index: int = None):
        if name:
            self.webdriver.switch_to.window(name)
        elif index >= 0:
            handle_name = self.all_window_handles[index]
            self.webdriver.switch_to.window(handle_name)

    def switch_frame(self, path: str, timeout: int = None) -> bool:
        """
        :Usage:
            driver.switch_frame("iframe[id=ifr]")
        """
        if not timeout: timeout = self.wait
        locator = self._detect_locator_type(path)
        frame = WebDriverWait(self.webdriver, timeout).until(ec.frame_to_be_available_and_switch_to_it(locator),
                                                             "Frame is not available")
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

    def alert(self, timeout: int = None) -> Alert:
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
        if not timeout: timeout = self.wait
        alert = WebDriverWait(self.webdriver, timeout).until(ec.alert_is_present(), "No alerts are present")
        return alert

    def basic_auth(self, url: str, username: str, password: str):
        """
        Basic javascript username:password URL authentication
        URL must contain protocol e.g. https
        """
        new_url = url.replace('//', f'//{username}:{password}@')
        self.get(new_url)

    def get(self, url: str):
        self.webdriver.get(url)

    def refresh(self):
        self.webdriver.refresh()

    def close(self):
        self.webdriver.close()

    def get_all_cookies(self):
        return self.webdriver.get_cookies()

    def add_cookie(self, cookie_dict: dict):
        """
        driver.add_cookie({"name" : "foo", "value" : "bar"})
        """
        self.webdriver.add_cookie(cookie_dict)

    def delete_cookie(self, name: str):
        """
        driver.delete_cookie("foo")
        """
        self.webdriver.delete_cookie(name)

    def delete_all_cookies(self):
        self.webdriver.delete_all_cookies()

    def session(self, path: str = "cookies.pkl"):
        """
        Save session cookies to specified path for later use if file path doesn't exist.
        Load session cookies from specified path otherwise.
        """
        if os.path.exists(path):
            with open(path, "rb") as f:
                cookies = pickle.load(f)
            [self.add_cookie(cookie) for cookie in cookies]
            self.refresh()
        else:
            input("Press ENTER once ready to save the session")
            cookies = self.get_all_cookies()
            with open(path, "wb") as f:
                pickle.dump(cookies, f)

    def screenshot(self, path: str = "screenshot.png"):
        self.webdriver.save_screenshot(path)

    def forward(self):
        self.webdriver.forward()

    def back(self):
        self.webdriver.back()

    def maximize(self):
        self.webdriver.maximize_window()

    def minimize(self):
        self.webdriver.minimize_window()

    def fullscreen(self):
        self.webdriver.fullscreen_window()

    def set_page_load_timeout(self, time: Union[int, float]):
        self.webdriver.set_page_load_timeout(time)

    def set_window_position(self, x: int, y: int, window_handle: str = None):
        self.webdriver.set_window_position(x, y, windowHandle=window_handle)

    def get_window_position(self, window_handle: str = None) -> dict:
        return self.webdriver.get_window_position(windowHandle=window_handle)

    def get_window_size(self, window_handle: str = None) -> dict:
        return self.webdriver.get_window_size(windowHandle=window_handle)

    def set_window_size(self, width: int, height: int, window_handle: str = None):
        self.webdriver.set_window_size(width, height, windowHandle=window_handle)

    def get_window_geometry(self) -> dict:
        return self.webdriver.get_window_rect()

    def quit(self):
        self.webdriver.quit()
