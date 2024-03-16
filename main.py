import platform
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.support.ui import Select
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def translate_text(text, translator, src='en', dest='ru'):
    try:
        return translator.translate(text, src=src, dest=dest).text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text

def main():
    driver = webdriver.Chrome()
    translator = Translator()
    all_results = []
    url = "https://registers.centralbank.ie/FirmSearchPage.aspx"
    driver.get(url)

    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1

    dropdown = Select(driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_ddlFirms'))
    
    for i in range(1, len(dropdown.options)):  # Start from 1 to skip 'All'
        driver.get(url)
        dropdown = Select(driver.find_element(By.ID, 'ctl00_cphRegistersMasterPage_ddlFirms'))
        dropdown.select_by_index(i)
        selected_type = dropdown.options[i].text

        search_button = driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_btnFirmNameSearch")
        search_button.click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults")))
        page_count_element = driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_lblPageCount")
        total_pages = int(page_count_element.text)

        for _ in range(total_pages):
            rows = driver.find_elements(By.CSS_SELECTOR, "#ctl00_cphRegistersMasterPage_gvwSearchResults tr:not(.searchresultsheader):not(.searchresultspager)")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    link = cells[1].find_element(By.TAG_NAME, "a")  # Assuming the link is in the second cell
                    # Determine the OS-specific key for the action
                    modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

                    # Perform a modifier key + click action to open the link in a new tab
                    action = ActionChains(driver)
                    action.key_down(modifier_key).click(link).key_up(modifier_key).perform()
                    time.sleep(2) 
                    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
                    for window_handle in driver.window_handles:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            break

                    # Assuming you're parsing a 'description' from the new window
                    try:
                        description_element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "f3_ctl00_cphRegistersMasterPage_c1wrptData"))
                        )
                        description = description_element.text
                    except Exception as e:
                        description = "Description not found."
                        print(f"Error finding description: {e}")

                    driver.close()
                    driver.switch_to.window(original_window)

                    entry = {
                        "Страна": "Ирландия",
                        "Тип": "white_list",
                        "Источник": url,
                        "Name": cells[1].text.strip(),
                        "Тип Организации": translate_text(selected_type, translator),
                        "Описание": translate_text(description, translator),
                    }
                    all_results.append(entry)

            # Click the next page button if there is more than one page
            print(all_results)
            if total_pages > 1:
                next_button = driver.find_element(By.ID, "ctl00_cphRegistersMasterPage_gvwSearchResults_ctl18_btnNext")
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(rows[0]))

    driver.quit()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
