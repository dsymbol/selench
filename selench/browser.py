from selenium import webdriver


class Browser:
    def __init__(self, browser, executable_path, headless, user_agent, incognito):
        self.executable_path = executable_path
        self.headless = headless
        self.user_agent = user_agent
        self.incognito = incognito
        self.browser = browser.lower()

    @property
    def browser(self):
        return self._browser

    @browser.setter
    def browser(self, b):
        if b == "chrome":
            self.opts = self.chrome_options()
            if not self.executable_path: self.executable_path = "chromedriver"
        elif b == "firefox":
            self.opts = self.firefox_options()
            if not self.executable_path: self.executable_path = "geckodriver"
        else:
            raise Exception("Browser unsupported by Selench")
        self._browser = b

    def firefox_options(self):
        opts = webdriver.FirefoxOptions()
        if self.user_agent:
            opts.set_preference("general.useragent.override", self.user_agent)
        if self.headless:
            opts.headless = True
        if self.incognito:
            opts.set_preference("browser.private.browsing.autostart", True)
        return opts

    def chrome_options(self):
        opts = webdriver.ChromeOptions()
        if self.user_agent:
            opts.add_argument(f"user-agent={self.user_agent}")
        if self.headless:
            opts.add_argument('headless')
        if self.incognito:
            opts.add_argument('--incognito')
        return opts

    def create_driver(self):
        if self.browser == "chrome":
            driver = webdriver.Chrome(executable_path=self.executable_path, options=self.opts)
        elif self.browser == "firefox":
            driver = webdriver.Firefox(executable_path=self.executable_path, options=self.opts)
        return driver
