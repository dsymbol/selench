# Selench

Selench is a wrapper that simplifies the use of the Selenium library. 
It provides a more concise syntax that makes the code more readable and easier to understand.

### Key Features

- Concise syntax
- Less imports
- Elements have an explicit wait time by default
- Simple expected_conditions implementation as expect
- Element type detection ( CSS & XPATH )

## Installation

To install the library, use pip:

```bash
pip install selench
```

Alternatively, install the latest directly from the GitHub repository:
```bash
pip install git+https://github.com/dsymbol/selench.git
```

## Examples

Navigate to DuckDuckGo and search for 'Hello World!'

```py
from selench import Selench, Keys

driver = Selench()
driver.get('https://duckduckgo.com')
driver.element('[name=q]').send_keys('Hello World!', Keys.ENTER)
driver.quit()
```

Using PyTest: navigate to DuckDuckGo and search for 'github' assert titles contain 'github'

```py
from selench import Selench, Keys
import pytest

@pytest.fixture
def driver():
    driver = Selench()
    yield driver
    driver.quit()

def test_ddg_search_query(driver):
    keyword = 'github'
    driver.get('https://duckduckgo.com/')
    driver.element('[name=q]').send_keys(keyword, Keys.ENTER)
    driver.expect.title_to_contain(keyword)
    titles = driver.elements('a[data-testid=result-title-a] span')

    for title in titles:
        assert keyword in title.text.lower()
```