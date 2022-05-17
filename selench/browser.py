from random import choice

from selenium import webdriver


class BrowserSetup:
    def __init__(self, browser, headless, incognito):
        self.headless = headless
        self.incognito = incognito
        self.browser = browser.lower()

    @property
    def browser(self):
        return self._browser

    @browser.setter
    def browser(self, b):
        if b == "chrome":
            self.opts = self.chrome_options()
        elif b == "firefox":
            self.opts = self.firefox_options()
        else:
            raise Exception("Browser unsupported by Selench")
        self._browser = b

    def firefox_options(self):
        opts = webdriver.FirefoxOptions()
        opts.set_preference("general.useragent.override", choice(USER_AGENTS))
        if self.headless:
            opts.headless = True
        if self.incognito:
            opts.set_preference("browser.private.browsing.autostart", True)
        return opts

    def chrome_options(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument(f"user-agent={choice(USER_AGENTS)}")
        if self.headless:
            opts.add_argument('headless')
        if self.incognito:
            opts.add_argument('--incognito')
        return opts

    def create_driver(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome(options=self.opts)
        if self.browser == "firefox":
            self.driver = webdriver.Firefox(options=self.opts)
        return self.driver


USER_AGENTS = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
    "54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safa"
    "ri/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41."
    "0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko"
    ") Chrome/42.0.2311.135 "
    "Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, "
    "like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
]
