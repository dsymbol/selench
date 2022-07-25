import os
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement


class Action:
    def __init__(self, driver):
        self._driver = driver

    def hover(self, element: WebElement):
        """
        Hover over web element
        """
        ActionChains(self._driver.webdriver).move_to_element(element).perform()

    def double_click(self, element: WebElement):
        """
        Double click web element
        """
        ActionChains(self._driver.webdriver).double_click(element).perform()

    def right_click(self, element: WebElement):
        """
        Right click web element
        """
        ActionChains(self._driver.webdriver).context_click(element).perform()

    def scroll_to_element(self, element: WebElement):
        """
        Scroll to web element
        """
        ActionChains(self._driver.webdriver).scroll_to_element(element).perform()

    def scroll_amount(self, x: int, y: int):
        """
        Pass in x, y value for how much to scroll in the right and down directions.
        Negative values represent left and up, respectively.
        """
        ActionChains(self._driver.webdriver).scroll_by_amount(x, y).perform()

    def scroll_to_page_bottom(self):
        """
        Scroll to bottom of page
        """
        self._driver.execute_js('window.scrollTo(0, document.body.scrollHeight)')

    def drag_and_drop(self, draggable: WebElement, droppable: WebElement, alternative=False):
        """
        If native selenium drag and drop doesn't work try the alternative method by passing alternative=True
        elements passed must be CSS elements.
        Credits: https://github.com/SeleniumHQ/selenium/issues/8003
        """
        if not alternative:
            ActionChains(self._driver.webdriver).click_and_hold(draggable).move_to_element(droppable).perform()
            ActionChains(self._driver.webdriver).release().perform()
        else:
            file_path = os.path.join(str(Path(os.path.abspath(__file__)).parents[0]), 'js', 'drag_and_drop.js')
            with open(file_path, "r") as f:
                javascript = f.read()
            self._driver.execute_js(javascript, draggable, droppable)
