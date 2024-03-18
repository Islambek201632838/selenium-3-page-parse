from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from parser.utils.page_scraper import PageScraper

class WebScraper(PageScraper):
    def __init__(self):
        super().__init__()  # Correctly call the superclass's __init__ method to initialize its properties, including 'driver'.

    def __open_website(self, url):
        self.driver.get(url)
        self.original_window = self.driver.current_window_handle

    def scrape_website(self, url, translator):
        self.url = url
        self.__open_website(url)
        all_results = []
        dropdown = Select(self.driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_ddlFirms'))
        for i in range(1, 2):  # Skip 'All' option len(dropdown.options)
            selected_type = self._select_dropdown_option(dropdown, i)
            self.selected_type = selected_type
            self._click_search()
            self._handle_second_window()
            self.second_window = self.driver.current_window_handle
            page_results = self.__get_web_results(translator)
            all_results.extend(page_results)
            self.driver.switch_to.window(self.original_window)
        return list(set(all_results))
        
    def __get_web_results(self, translator):
        results = []
        page_results = self._scrape_current_page(translator)
        results.extend(page_results)
        self.driver.close()  # Close the newly opened window.
        self.driver.switch_to.window(self.original_window)  # Switch back to the original window.
        return results

    def __del__(self):
            self.driver.quit()
