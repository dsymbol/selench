from selenium.common import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec

from .element import Element


class Expect:
    """
    This class provides methods for waiting for certain conditions to be met in a web page
    using Selenium's WebDriverWait and ExpectedConditions.
    """

    def __init__(self, driver):
        self._driver = driver

    def element_to_be_clickable(self, mark: Element | str) -> None:
        """
        An Expectation for checking an element is visible and enabled such that you can click it.

        Args:
            mark: Either a selector or an Element.

        Raises:
            TimeoutException: If the element is not clickable.
        """
        locator = (
            mark.webelement
            if isinstance(mark, Element)
            else self._driver._detect_selector(mark)
        )
        self._driver.wait.until(
            ec.element_to_be_clickable(locator), "Element is not clickable"
        )

    def element_to_be_visible(self, selector: str) -> None:
        """
        An expectation for checking that an element is present on the DOM of a page and visible.
        Visibility means that the element is not only displayed but also has a height and width
        that is greater than 0.

        Args:
            selector: The selector of the element.

        Raises:
            TimeoutException: If the element is not visible within the given timeout.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.visibility_of_element_located(locator), "Element is not visible"
        )

    def elements_to_be_visible(self, selector: str) -> None:
        """
        An expectation for checking that all elements are present on the DOM of a page and visible.
        Visibility means that the elements are not only displayed but also has a height and width
        that is greater than 0.

        Args:
            selector: The selector of the elements to wait for.

        Raises:
            TimeoutException: If the element are not visible within the given timeout.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.visibility_of_all_elements_located(locator),
            "Not all elements are visible",
        )

    def element_to_be_invisible(self, mark: Element | str) -> None:
        """
        An Expectation for checking that an element is either invisible or not present on the DOM.

        Args:
            mark: Either a selector or an Element.

        Raises:
            TimeoutException: If the element is not invisible within the given timeout.
        """
        locator = (
            mark.webelement
            if isinstance(mark, Element)
            else self._driver._detect_selector(mark)
        )
        self._driver.wait.until(
            ec.invisibility_of_element_located(locator), "Element is not invisible"
        )

    def elements_to_be_invisible(self, selector: str) -> None:
        """
        An Expectation for checking that all elements are either invisible or not present on the DOM.

        Args:
            selector: The selector of the elements to wait for.

        Raises:
            TimeoutException: If the elements are not invisible within the given timeout.
        """

        def invisibility_of_all_elements_located(locator):

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

        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            invisibility_of_all_elements_located(locator), "Elements are not invisible"
        )

    def element_to_be_stale(self, element: Element) -> None:
        """
        Wait until an element is no longer attached to the DOM. element is the element to wait for.

        Args:
            element: The Element to wait for.

        Raises:
            TimeoutException: If the element is not stale.
        """
        self._driver.wait.until(
            ec.staleness_of(element.webelement), "Element did not go stale"
        )

    def element_to_have_text(self, selector: str) -> None:
        """
        An expectation for checking if text is present in the specified element.

        Args:
            selector: The selector of the element.

        Raises:
            TimeoutException: If the element does not contain text.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            lambda d: bool(d.find_element(*locator).text), "No text in element"
        )

    def element_text_to_contain(self, selector: str, text: str) -> None:
        """
        An expectation for checking if the given text is present in the specified element.

        Args:
            selector: The selector of the element.
            text: The text to search for in the selected element's text.

        Raises:
            TimeoutException: If the element does not contain text.

        Example::

            driver.expect.element_text_to_contain('//div[@id="msg"]', 'welcome')
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.text_to_be_present_in_element(locator, text),
            f"Element text is not `{text}`",
        )

    def element_text_to_be(self, selector: str, text: str) -> None:
        """
        An expectation for checking if the given text exactly matches the text within the specified element.

        Args:
            selector: The selector of the element.
            text: The expected text to be present within the element.

        Example::

            driver.expect.element_text_to_be('#my-element', 'Hello')
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            lambda d: bool(d.find_element(*locator).text == text),
            f"Element text doesn't match {text}",
        )

    def element_attribute_text_to_contain(
        self, selector: str, attribute: str, text: str
    ) -> None:
        """
        An expectation for checking if the given text is present in the element’s attribute.

        Args:
            selector: The selector of the element.
            attribute: The name of the attribute to check for the presence of the given text.
            text: The text to search for in the selected element's attribute.

        Raises:
            TimeoutException: If the element's attribute does not contain text.

        Example::

            driver.expect.element_attribute_text_to_contain('//div[@id="msg"]', 'value', 'new message')
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.text_to_be_present_in_element_attribute(locator, attribute, text),
            "Text is not present in attribute",
        )

    def element_to_be_checked(self, selector: str) -> None:
        """
        An expectation to locate an element and check if it's checked.

        Args:
            selector: The selector of the element.

        Raises:
            TimeoutException: if the selection state specified is not in that state.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.element_located_selection_state_to_be(locator, True),
            "Element is not checked",
        )

    def element_to_not_be_checked(self, selector: str) -> None:
        """
        An expectation to locate an element and check if it's not checked.

        Args:
            selector: The selector of the element.

        Raises:
            TimeoutException: if the selection state specified is not in that state.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.element_located_selection_state_to_be(locator, False),
            "Element is checked",
        )

    def element_to_be_present(self, selector: str) -> None:
        """
        An expectation for checking that an element is present on the DOM of a page.

        Args:
            selector: The selector of the element.

        Raises:
            TimeoutException: If the element is not present on the DOM.
        """
        locator = self._driver._detect_selector(selector)
        self._driver.wait.until(
            ec.presence_of_element_located(locator), "Element is not present on the DOM"
        )

    def url_to_be(self, url: str) -> None:
        """
        An expectation for checking the current url is the expected url, which must be an exact match.

        Args:
            url: The expected url.

        Raises:
            TimeoutException: if current url is not the expected url.
        """
        self._driver.wait.until(ec.url_to_be(url), f"{url} != {self._driver.url}")

    def url_to_contain(self, string: str) -> None:
        """
        An expectation for checking that the current url contains a case-sensitive substring.

        Args:
            string: The expected case-sensitive substring.

        Raises:
            TimeoutException: if the current url does not contain the string.
        """
        self._driver.wait.until(
            ec.url_contains(string), f"`{self._driver.url}` does not contain `{string}`"
        )

    def title_to_be(self, title: str) -> None:
        """
        An expectation for checking the title of a page. title is the expected title, which must be an exact match.

        Args:
            title: The expected title.

        Raises:
            TimeoutException: if the title doesn't match.
        """
        self._driver.wait.until(ec.title_is(title), f"`{title} != {self._driver.title}")

    def title_to_contain(self, string: str) -> None:
        """
        An expectation for checking that the title contains a case-sensitive substring.

        Args:
            string: The expected case-sensitive substring.

        Raises:
            TimeoutException: if the current title does not contain the string.
        """
        self._driver.wait.until(
            ec.title_contains(string),
            f"`{self._driver.title}` does not contain `{string}`",
        )
