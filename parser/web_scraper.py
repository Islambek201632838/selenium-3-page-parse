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
        try:
            dropdown = Select(self.driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_ddlFirms'))
            for i in range(1, len(dropdown.options)): 
                print(f"dropdown index: {i}")
                selected_type = self._select_dropdown_option(dropdown, i)
                self.selected_type = selected_type
                self._click_search()
                self._handle_second_window()
                self.second_window = self.driver.current_window_handle
                page_results = self.__get_web_results(translator)
                all_results.extend(page_results)
                self.driver.close()
                self.driver.switch_to.window(self.original_window)
            return list(set(all_results))
        except Exception as e:
             print(f"No dropdown found or another error {e}")
             return []
        
    def __get_web_results(self, translator):
        results = []
        page_results = self._scrape_current_page(translator)
        results.extend(page_results)
        return results

    def __del__(self):
            self.driver.quit()
