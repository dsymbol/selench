# Selench

Selench is a Python WebDriver wrapper that simplifies the use of the Selenium library. 
It provides a more concise syntax that makes the code more readable and easier to understand.

### Key Features

- Elements have an explicit wait time by default
- Element type detection ( CSS & XPATH )

## Installation

The easiest way to install the latest version from PyPI is by using
[pip](https://pip.pypa.io/):

```bash
pip install selench
```

Alternatively, install directly from the GitHub repository:
```bash
pip install git+https://github.com/dsymbol/selench.git
```

## Documentation

The documentation can be found at https://dsymbol.github.io/selench/

## Examples

Here are some examples of how to use Selench:

```py
from selench import Selench, Keys

# Create a new Selench instance
driver = Selench()

# Navigate to google
driver.get('https://google.com')

# Search google for 'Hello World!'
driver.element('input[name="q"]').send_keys('Hello World!', Keys.ENTER)

# Quit the driver
driver.quit()
```

Using PyTest:

```py
from selench import Selench, Keys
import pytest

# Create a fixture to provide the driver instance to the test functions
@pytest.fixture
def driver():
    driver = Selench()
    yield driver
    driver.quit()

def test_ddg_search_query(driver):
    # Define a search query
    keyword = 'github'
    
    # Navigate to duckduckgo
    driver.get('https://duckduckgo.com/')
    
    # Search duckduckgo for the keyword
    driver.element('*[name="q"]').send_keys(keyword, Keys.ENTER)
    
    # Wait for the page title to contain the keyword
    driver.wait_for.title_to_contain(keyword)
    
    # Find all the result titles
    titles = driver.elements('a[data-testid="result-title-a"] span')

    # Check that the keyword is present in each title
    for title in titles:
        assert keyword in title.text.lower()
```