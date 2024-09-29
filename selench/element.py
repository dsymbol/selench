from typing import List

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Element:
    def __init__(self, driver, webelement: WebElement, locator: tuple[str, str]):
        self._driver = driver
        self._webelement = webelement
        self._locator = locator
        self._by, self._selector = locator

    @property
    def webelement(self):
        """
        This property provides access to the underlying WebElement instance.
        Can be used to access webelement's methods and properties that are not yet implemented in this package.

        Returns:
            WebElement instance

        >>> element = driver.element("button")
        >>> element.webelement.click()
        """
        return self._webelement

    @property
    def text(self) -> str:
        """
        Returns:
            The text of the element.
        """
        return self.webelement.text

    def click(self) -> "Element":
        """
        Clicks the element.

        Returns:
            The instance of Element (self).
        """
        self.webelement.click()
        return self

    def send_keys(self, *values: str) -> "Element":
        """
        Simulates typing into the element.

        Returns:
            The instance of Element (self).
        """
        self.webelement.send_keys(*values)
        return self
    
    fill = send_keys

    def clear(self) -> "Element":
        """
        Clears the text if it's a text entry element.

        Returns:
            The instance of Element (self).
        """
        self.webelement.clear()
        return self

    def element(self, selector: str, timeout: int = None) -> "Element":
        """
        Identifies the type of the provided selector and returns the first matching element.

        Args:
            selector: The selector for the element.
            timeout: The time to wait for the element to be found.

        Returns:
            The found Element.

        Raises:
            Exception: If the element is not found.
        """
        wait = (
            WebDriverWait(self._driver.webdriver, timeout)
            if timeout
            else self._driver.wait
        )
        locator = self._driver._detect_selector(selector)
        element = wait.until(
            lambda _: self.webelement.find_element(*locator),
            f"Could not find element with the {locator}",
        )
        return Element(self._driver, element, locator)

    def elements(self, selector: str, timeout: int = None) -> List["Element"]:
        """
        Identifies the type of the provided selector and returns a list of matching element.

        Args:
            selector: The selector for the elements.
            timeout: The time to wait for the elements to be found.

        Returns:
            A list of the found Elements. If no elements are found, an empty list is returned.
        """
        wait = (
            WebDriverWait(self._driver.webdriver, timeout)
            if timeout
            else self._driver.wait
        )
        try:
            locator = self._driver._detect_selector(selector)
            elements = wait.until(
                lambda _: self.webelement.find_elements(*locator),
                f"Could not find elements with the {locator}",
            )
            elements = [Element(self._driver, element, locator) for element in elements]
        except TimeoutException:
            elements = []
        return elements

    def submit(self) -> "Element":
        """
        Submits a form.

        Returns:
            The instance of Element (self).
        """
        self.webelement.submit()
        return self

    def is_displayed(self) -> bool:
        """
        Whether the element is visible.

        Returns:
            True if the element is displayed otherwise False.
        """
        return self.webelement.is_displayed()
    
    is_visible = is_displayed

    def is_enabled(self) -> bool:
        """
        Whether the element is enabled.

        Returns:
            True if the element is enabled otherwise False.
        """
        return self.webelement.is_enabled()

    def is_selected(self) -> bool:
        """
        Whether the element is selected.

        Returns:
            True if the element is selected otherwise False.
        """
        return self.webelement.is_selected()

    def get_property(self, name: str) -> str:
        """
        Gets the given property of the element.

        Returns:
            The given property of the element.
        """
        return self.webelement.get_property(name)
    
    get_attribute = get_property

    def hover(self) -> "Element":
        """
        Move the mouse cursor over the web element.

        Returns:
            The instance of Element (self).
        """
        ActionChains(self._driver.webdriver).move_to_element(self.webelement).perform()
        return self

    def double_click(self) -> "Element":
        """
        Perform a double click on the web element.

        Returns:
            The instance of Element (self).
        """
        ActionChains(self._driver.webdriver).double_click(self.webelement).perform()
        return self

    def right_click(self) -> "Element":
        """
        Perform a right click on the web element.

        Returns:
            The instance of Element (self).
        """
        ActionChains(self._driver.webdriver).context_click(self.webelement).perform()
        return self

    def scroll_to(self) -> "Element":
        """
        Scroll the page to the web element.

        Returns:
            The instance of Element (self).
        """
        ActionChains(self._driver.webdriver).scroll_to_element(
            self.webelement
        ).perform()
        return self

    def drag_to(self, target: "Element") -> "Element":
        """
        Perform a drag and drop action to the provided element.

        Args:
            target: The element to be dropped on.

        Returns:
            The instance of Element (self).
        """
        ActionChains(self._driver.webdriver).click_and_hold(
            self.webelement
        ).move_to_element(target.webelement).perform()
        ActionChains(self._driver.webdriver).release().perform()
        return self

    def select_by_index(self, index: int) -> "Element":
        """
        Select an option based upon the internal index.

        Returns:
            The instance of Element (self).
        """
        Select(self.webelement).select_by_index(index)
        return self

    def select_by_value(self, value: str) -> "Element":
        """
        Select an option based upon its value attribute.

        Returns:
            The instance of Element (self).
        """
        Select(self.webelement).select_by_value(value)
        return self

    def select_by_visible_text(self, text: str) -> "Element":
        """
        Select an option based upon its visible text.

        Returns:
            The instance of Element (self).
        """
        Select(self.webelement).select_by_visible_text(text)
        return self

    def screenshot(self, path: str = "screenshot.png") -> bool:
        """
        Saves a screenshot of the current element to a PNG image file.

        Args:
            path: The file path to save the screenshot. Default is "screenshot.png"

        Returns:
            False if there is any IOError otherwise True.
        """
        return self.webelement.screenshot(path)
