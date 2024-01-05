import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
import time
import json

link_url = "https://www.mercateo.com/kw/4051428062220/4051428062220.html?ViewName=live~secureMode&switchToCountry=DE&switchToLanguage=de&chooseGeo=true"

def validate_map (link_url):
    options = Options()
    # options.headless = False
    driver = webdriver.Firefox(options=options)
    driver.get(link_url)
    try:
        wait_time_out = 15
        wait_variable = WebDriverWait(driver, wait_time_out)
        maps = wait_variable.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "map")))

        if maps:
            # Assuming you want to find the "DE" link within the first map element
            map_element = maps[0]
            link = map_element.find_element(By.ID, "DE")
            
            if link:
                link_url = link.get_attribute("href")
                print("Link URL:", link_url)
                driver.get(link_url)


            else:
                print("Link with ID 'DE' not found within the first map.")
        else:
            print("No map elements found.")

    except NoSuchElementException:
        print('No such element')
    except TimeoutException:
        print('Element "DE" not clickable within the specified timeout')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    return driver


def noSearchResults(driverObject, ean):
    try:
        no_result_table = driverObject.find_elements(By.CSS_SELECTOR, 'table.BD05.fs_2')
        if no_result_table:
            for result in no_result_table:
                table_body = result.find_elements(By.TAG_NAME, 'tbody')
                for table_row in table_body:
                    rows = table_row.find_elements(By.TAG_NAME, 'tr')
                    if len(rows) == 3:
                        no_search_suggestion = rows[0].find_elements(By.CSS_SELECTOR, 'div.m5.fw_b')
                        if len(no_search_suggestion) == 1:
                            if no_search_suggestion[0].text:
                                return None
                        else:
                            return 'not none'
                    else:
                        return 'not none'
        else:
            return 'not none'

    except:
        return 'returned'


if __name__=="__main__":
    options = Options()
    # options.headless = False
    driver = webdriver.Firefox(options=options)
    driver.get(link_url)
    table = driver.find_element(By.CSS_SELECTOR, "table#pl_l_p_1.fs_2.BD05.bw_1001")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        if row.get_attribute('class'):
            anchor = row.find_element(By.CSS_SELECTOR, "a.fs_2.hc_3.c_1.plvistedeffect.plhovereffect")
            link = anchor.get_attribute('href')
            print(link)
            driver.get(link)
        break