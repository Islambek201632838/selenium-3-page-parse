from selenium import webdriver

class SetUp:
    @staticmethod
    def setup_webdriver():
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=options)