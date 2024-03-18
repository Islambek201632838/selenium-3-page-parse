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

        try:
            page_count_element = self.driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_lblPageCount")
            total_pages = int(page_count_element.text)
        except Exception as e:
            print("Page count element is not found or page count is 1")
            print(e)
            total_pages = 1

        for current_page in range(1, total_pages + 1):
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults")))
                rows = self.driver.find_elements(By.CSS_SELECTOR, "#ctl00_cphRegistersMasterPage_gvwSearchResults tr:not(.searchresultsheader):not(.searchresultspager)")
                print(f"current page: {current_page}")
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
                    # put break if you want test faster. you dont need to iterate over all rows

                if  current_page < total_pages:
                    try:
                        next_button = self.driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_btnNext")
                        next_button.click()
                        WebDriverWait(self.driver, 10).until(EC.staleness_of(rows[0]))
                    except:
                        print("next button not found")
            except Exception as e:
                results = []
                print(f"No table found or another error {e}")

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

