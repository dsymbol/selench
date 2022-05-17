import pytest

from selench import Selench


@pytest.fixture
def driver():
    driver = Selench()
    yield driver
    driver.quit()
