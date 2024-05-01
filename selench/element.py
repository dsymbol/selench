from typing import List

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


class Element:
    def __init__(self, driver, webelement: WebElement, locator: tuple[str, str]):
        self._driver = driver
        self._webelement = webelement
        self._locator = locator
        self._by, self._selector = locator

    @property
    def webelement(self):
        """
        This property provides access to the underlying webelement instance.
        Can be used to access webelement's methods and properties that are not yet implemented in this package.

        Returns:
            webelement instance
        """
        return self._webelement

    @property
    def text(self) -> str:
        """
        The text of the element.
        """
        return self.webelement.text

    def element(self, selector: str) -> "Element":
        """
        Identifies the type of the provided selector and find the first matching element.

        Args:
            selector: The selector for the element.

        Returns:
            The found Element.

        Raises:
            Exception: If the element is not found.
        """
        locator = self._driver._detect_selector(selector)
        element = self._driver.wait.until(
            lambda _: self.webelement.find_element(*locator),
            f"Could not find element with the {locator}",
        )
        return Element(self._driver, element, locator)

    def elements(self, selector: str) -> List["Element"]:
        """
        Identifies the type of the provided selector and find a list of matching element.

        Args:
            selector: The selector for the elements.

        Returns:
            A list of the found Elements. If no elements are found, an empty list is returned.
        """
        try:
            locator = self._driver._detect_selector(selector)
            elements = self._driver.wait.until(
                lambda _: self.webelement.find_elements(*locator),
                f"Could not find elements with the {locator}",
            )
            elements = [Element(self._driver, element, locator) for element in elements]
        except TimeoutException:
            elements = []
        return elements

    def click(self) -> "Element":
        """
        Clicks the element.
        """
        self.webelement.click()
        return self

    def send_keys(self, *values: str) -> "Element":
        """
        Simulates typing into the element.
        """
        self.webelement.send_keys(*values)
        return self

    def clear(self) -> "Element":
        """
        Clears the text if it's a text entry element.
        """
        self.webelement.clear()
        return self

    def submit(self) -> "Element":
        """
        Submits a form.
        """
        self.webelement.submit()
        return self

    def is_displayed(self) -> bool:
        """
        Whether the element is visible.
        """
        return self.webelement.is_displayed()

    def visible(self) -> bool:
        """
        Whether the element is visible.
        """
        return self.webelement.is_displayed()

    def is_enabled(self) -> bool:
        """
        Whether the element is enabled.
        """
        return self.webelement.is_enabled()

    def is_selected(self) -> bool:
        """
        Whether the element is selected.
        """
        return self.webelement.is_selected()

    def get_property(self, name: str) -> str:
        """
        Gets the given property of the element.
        """
        return self.webelement.get_property(name)

    def hover(self) -> "Element":
        """
        Move the mouse cursor over the web element.
        """
        ActionChains(self._driver.webdriver).move_to_element(self.webelement).perform()
        return self

    def double_click(self) -> "Element":
        """
        Perform a double click on the web element.
        """
        ActionChains(self._driver.webdriver).double_click(self.webelement).perform()
        return self

    def right_click(self) -> "Element":
        """
        Perform a right click on the web element.
        """
        ActionChains(self._driver.webdriver).context_click(self.webelement).perform()
        return self

    def scroll_to(self) -> "Element":
        """
        Scroll the page to the web element.
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
        """
        ActionChains(self._driver.webdriver).click_and_hold(
            self.webelement
        ).move_to_element(target.webelement).perform()
        ActionChains(self._driver.webdriver).release().perform()
        return self

    def select_by_index(self, index: int) -> "Element":
        """
        Select an <option> based upon the <select> element's internal index.
        """
        Select(self.webelement).select_by_index(index)
        return self

    def select_by_value(self, value: str) -> "Element":
        """
        Select an <option> based upon its value attribute.
        """
        Select(self.webelement).select_by_value(value)
        return self

    def select_by_visible_text(self, text: str) -> "Element":
        """
        Select an <option> based upon its value attribute.
        """
        Select(self.webelement).select_by_visible_text(text)
        return self

    def screenshot(self, path: str = "screenshot.png") -> bool:
        """
        Saves a screenshot of the current element to a PNG image file.

        Args:
            path: The file path to save the screenshot. Default is "screenshot.png"

        Returns:
            Returns False if there is any IOError, else returns True.
        """
        return self.webelement.screenshot(path)
