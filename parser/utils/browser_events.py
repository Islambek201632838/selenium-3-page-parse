from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import platform
from parser.utils.window import HandleWindow

class BrowserEvents(HandleWindow):
    def __init__(self):
        super().__init__()  # Ensure proper initialization of HandleWindow and its properties, including the driver.

    def _select_dropdown_option(self, dropdown, index):
        dropdown.select_by_index(index)
        selected_option_text = dropdown.options[index].text
        return selected_option_text

    def _click_search(self):
        search_button = self.driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_btnFirmNameSearch")
        modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
        action = ActionChains(self.driver)
        action.key_down(modifier_key).click(search_button).key_up(modifier_key).perform()
        time.sleep(2) 

    def _click_link(self, cells):
            link = cells[1].find_element(By.TAG_NAME, "a")
            # Determine the modifier key based on the operating system.
            modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
            action = ActionChains(self.driver)
            action.key_down(modifier_key).click(link).key_up(modifier_key).perform()
            time.sleep(2)
            # Waiting for the new window to open and then switch to it.
            
    def _get_description(self):
        try:
            description_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "f3_ctl00_cphRegistersMasterPage_c1wrptData"))
            )
            description = description_element.text
        except Exception as e:
            description = "Description not found."
            print(f"Error finding description: {e}")

        return description
