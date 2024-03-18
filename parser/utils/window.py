from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from parser.utils.setup import SetUp

class HandleWindow(SetUp):
    def __init__(self):
        self.driver = self.setup_webdriver() 
        
    def _handle_third_window(self):
        WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(3))
        for handle in self.driver.window_handles:
            if handle not in [self.original_window, self.second_window]:
                self.driver.switch_to.window(handle)
                break
    
    def _handle_second_window(self):
        WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))
        for handle in self.driver.window_handles:
            if handle != self.original_window:
                self.driver.switch_to.window(handle)
                break