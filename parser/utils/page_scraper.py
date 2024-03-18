from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from parser.utils.browser_events import BrowserEvents

class PageScraper(BrowserEvents):
    def __init__(self):
        super().__init__() 
        self.all_results = []
    def _scrape_current_page(self, translator):
        results = []
        total_pages = 1
        # try:
        #     page_count_element = self.driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_lblPageCount")
        #     total_pages = int(page_count_element.text)
        # except Exception as e:
        #     print(f"Pagination not found or single page results: {e}")

        for current_page in range(total_pages):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults")))
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#ctl00_cphRegistersMasterPage_gvwSearchResults tr:not(.searchresultsheader):not(.searchresultspager)")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    name = cells[1].text.strip()
                    self._click_link(cells)
                self._handle_third_window()
                self.description = self._get_description()
                
                page_result = self.__set_page_results(translator, name, self.description)
                results.extend(page_result)
                
                self.driver.close() 
                self.driver.switch_to.window(self.second_window)
            
 
            if total_pages > 1:
                next_button = self.driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_btnNext")
                next_button.click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(rows[0]))
        
        self.driver.close() 
        self.driver.switch_to.window(self.original_window)
        
        return results
    
    def __set_page_results(self, translator, name, description):
        description_translated = translator.translate_text(description)
        type_translated = translator.translate_text(self.selected_type)

        return [{
            "Страна": "Ирландия",
            "Тип": "white_list",
            "Источник": self.url, 
            "Имя": name,
            "Описание": description_translated,
            "Тип Организации": type_translated
        }]

