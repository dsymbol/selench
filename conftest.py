import pytest

from selench import Selench


@pytest.fixture
def driver():
    driver = Selench("Edge")
    yield driver
    driver.quit()
