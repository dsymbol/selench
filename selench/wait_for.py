from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class WaitFor:
    """
    This class provides methods for waiting for certain conditions to be met in a web page
    using Selenium's WebDriverWait and ExpectedConditions.
    """
    def __init__(self, driver):
        self._driver = driver

    def element_clickable(self, selector: str, timeout: int = None) -> WebElement:
        """
        An Expectation for checking an element is visible and enabled such that you can click it.

        Args:
            selector: The selector of the element to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            The clickable element.

        Raises:
            Exception: If the element is not clickable.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.element_to_be_clickable(locator),
                                                                       "Element is not clickable")
        return element

    def element_visibility(self, selector: str, timeout: int = None) -> WebElement:
        """
        An expectation for checking that an element is present on the DOM of a page and visible.
        Visibility means that the element is not only displayed but also has a height and width
        that is greater than 0.

        Args:
            selector: The selector of the element to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            The located and visible element.

        Raises:
            Exception: If the element is not visible within the given timeout.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.visibility_of_element_located(locator),
                                                                       "Element is not visible")
        return element

    def elements_visibility(self, selector: str, timeout: int = None) -> List[WebElement]:
        """
        An expectation for checking that all elements are present on the DOM of a page and visible.
        Visibility means that the elements are not only displayed but also has a height and width
        that is greater than 0.

        Args:
            selector: The selector of the elements to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            A list of located and visible elements.

        Raises:
            Exception: If the element are not visible within the given timeout.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        elements = WebDriverWait(self._driver.webdriver, timeout).until(ec.visibility_of_all_elements_located(locator),
                                                                        "Not all elements are visible")
        return elements

    def element_invisibility(self, selector: str, timeout: int = None) -> WebElement:
        """
        An Expectation for checking that an element is either invisible or not present on the DOM.

        Args:
            selector: The selector of the element to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            The invisible element.

        Raises:
            Exception: If the element is not invisible within the given timeout.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.invisibility_of_element_located(locator),
                                                                       "Element is not invisible")
        return element

    def elements_invisibility(self, selector: str, timeout: int = None) -> List[WebElement]:
        """
        An Expectation for checking that elements are either invisible or not present on the DOM.

        Args:
            selector: The selector of the elements to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            A list of invisible elements.

        Raises:
            Exception: If the elements are not invisible within the given timeout.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        elements = WebDriverWait(self._driver.webdriver, timeout).until(
            self._visibility_of_all_elements_located(locator), "Elements are not invisible")
        return elements

    def element_staleness(self, element: WebElement, timeout: int = None) -> bool:
        """
        Wait until an element is no longer attached to the DOM. element is the element to wait for.

        Args:
            element: The WebElement to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the element is no longer attached to the DOM.

        Raises:
            Exception: If the element is not stale.
        """
        if not timeout: timeout = self._driver.wait
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.staleness_of(element),
                                                                       "Element did not go stale")
        return element

    def element_text(self, selector: str, timeout: int = None) -> bool:
        """
        An expectation for checking if text is present in the specified element.

        Args:
            selector: The selector of the element to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if text is present in the element.

        Raises:
            Exception: If the element does not contain text.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(lambda d: bool(d.find_element(*locator).text),
                                                                       "No text in element")
        return element

    def element_text_to_include(self, selector: str, text: str, timeout: int = None) -> bool:
        """
        An expectation for checking if the given text is present in the specified element.

        Args:
            selector: The selector of the element.
            text: The text to search for in the selected element's text.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if text is present in the element.

        Raises:
            Exception: If the element does not contain text.

        Example::

            driver.wait_for.element_text_to_be('//div[@id="msg"]', 'welcome')
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.text_to_be_present_in_element(locator, text),
                                                                       f"Element text is not `{text}`")
        return element

    def element_attribute_text_to_include(self, selector: str, attribute: str, text: str, timeout: int = None) -> bool:
        """
        An expectation for checking if the given text is present in the element’s attribute.

        Args:
            selector: The selector of the element.
            attribute: The name of the attribute to check for the presence of the given text.
            text: The text to search for in the selected element's attribute.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if text is present in the attribute.

        Raises:
            Exception: If the element's attribute does not contain text.

        Example::

            driver.wait_for.element_attribute_text_to_include('//div[@id="msg"]', 'value', 'new message')
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.text_to_be_present_in_element_attribute(
            locator, attribute, text), "Text is not present in attribute"
        )
        return element

    def element_selection_state(self, selector: str, is_selected: bool, timeout: int = None) -> bool:
        """
        An expectation to locate an element and check if the selection state specified is in that state.

        Args:
            selector: The selector of the element to wait for.
            is_selected: True for checked False otherwise.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the selection state specified is in that state.

        Raises:
            Exception: if the selection state specified is not in that state.

        Example::

            driver.wait_for.element_selection_state('input[type="checkbox"]', False)
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(
            ec.element_located_selection_state_to_be(locator, is_selected),
            "Element is not selected" if is_selected else "Element is selected")
        return element

    def element_presence(self, selector: str, timeout: int = None) -> WebElement:
        """
        An expectation for checking that an element is present on the DOM of a page.

        Args:
            selector: The selector of the element to wait for.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            The DOM present element.

        Raises:
            Exception: If the element is not present on the DOM.
        """
        if not timeout: timeout = self._driver.wait
        locator = self._driver._detect_locator_type(selector)
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.presence_of_element_located(locator),
                                                                       "Element is not present on the DOM")
        return element

    def url_to_be(self, url: str, timeout: int = None) -> bool:
        """
        An expectation for checking the current url is the expected url, which must be an exact match.

        Args:
            url: The expected url.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the current url is the expected url.

        Raises:
            Exception: if current url is not the expected url.
        """
        if not timeout: timeout = self._driver.wait
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.url_to_be(url),
                                                                       f"{url} != {self._driver.url}")
        return element

    def url_to_include(self, string: str, timeout: int = None) -> bool:
        """
        An expectation for checking that the current url contains a case-sensitive substring.

        Args:
            string: The expected case-sensitive substring.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the current url contains the string.

        Raises:
            Exception: if the current url does not contain the string.
        """
        if not timeout: timeout = self._driver.wait
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.url_contains(string),
                                                                       f"`{self._driver.url}` does not contain `{string}`")
        return element

    def title_to_be(self, title: str, timeout: int = None) -> bool:
        """
        An expectation for checking the title of a page. title is the expected title, which must be an exact match.

        Args:
            title: The expected title.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the title matches.

        Raises:
            Exception: if the title doesn't match.
        """
        if not timeout: timeout = self._driver.wait
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.title_is(title),
                                                                       f"`{title} != {self._driver.title}")
        return element

    def title_to_contain(self, string: str, timeout: int = None) -> bool:
        """
        An expectation for checking that the title contains a case-sensitive substring.

        Args:
            string: The expected case-sensitive substring.
            timeout: Maximum time to wait in seconds. Default is None, which means use the default wait time.

        Returns:
            True if the current title contains the string.

        Raises:
            Exception: if the current title does not contain the string.
        """
        if not timeout: timeout = self._driver.wait
        element = WebDriverWait(self._driver.webdriver, timeout).until(ec.title_contains(string),
                                                                       f"`{self._driver.title}` does not contain `{string}`")
        return element

    """
     * Custom "Expected Conditions" *
    """

    @staticmethod
    def _visibility_of_all_elements_located(locator):

        def _predicate(driver):
            try:
                elements = driver.find_elements(*locator)
                for element in elements:
                    if element.is_displayed():
                        return False
                return elements
            except StaleElementReferenceException:
                return False

        return _predicate
