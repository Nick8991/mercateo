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
# from selenium.webdriver.common.keys import Keys


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

def chooserightFrame(driverObject, i):
    try:
        # Find all select elements on the page
        wait_time_out = 5
        wait_variable = WebDriverWait(driverObject, wait_time_out)
        select_element = wait_variable.until(EC.visibility_of_all_elements_located((By.NAME, "ncID")))
        options = select_element[0].find_elements(By.TAG_NAME, 'option')
        options[i].click()
        wait_variable = WebDriverWait(driverObject, 2)

        # Wait for the page to refresh or perform further actions as needed
        wait_time_out = 2
        wait_variable = WebDriverWait(driverObject, wait_time_out)
        table = wait_variable.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.fs_2.BD05.bw_0001")))
        if table:
            return (driverObject,2)
        else:
            return (driverObject,None)

    except TimeoutException as e:
        print(e)
        return (driverObject,1)  # Add this line to return 1 when NoSuchElementException occurs


def getLastAppended(file_name):
    try:
        with open(file_name, 'r', encoding='utf_8') as json_file:
            lines = json_file.readlines()
            if not lines:
                return None
            last_line = lines[-1]
            last_element = json.loads(last_line)
            return last_element
    except FileNotFoundError:
        return None
    


def getFeatures(driverObject, mydict,file_name,ean):
    table = driverObject.find_elements(By.CSS_SELECTOR, 'table.fs_2.BD05.bw_0001')
    if table:
        table_rows = table[0].find_elements(By.TAG_NAME, 'tr')

        for i, row in enumerate(table_rows):
            if row.get_attribute('class'):
                text_divs = row.find_elements(By.TAG_NAME, 'div')
                dict_key = text_divs[0].text
                dict_value = text_divs[1].text
                print(dict_key, dict_value)
                mydict[dict_key] = dict_value

            else:
                pass

        print(mydict)
        mydict['ean'] = ean
        appenddictoJson(file_name,mydict)


def main(ean,features_dict):
    url_link = f'https://www.mercateo.com/kw/{ean}/{ean}.html?ViewName=live~secureMode'
    driverObject1 = validate_map(url_link)
    results = noSearchResults(driverObject1, ean)
    if results is None:
        print('no search results')
        driverObject1.close()
    else:
        for i in range(2):
            product_information = chooserightFrame(driverObject1,i)
            if product_information[1] == 2:
                found_product_information = False
                break
            elif product_information[1] == 1:
                found_product_information = False
        if not found_product_information:   
            getFeatures(product_information[0], features_dict,file_name,ean)
        product_information[0].close()


def appenddictoJson(file_name, feature_dict):
    with open(file_name, 'a',encoding='utf-8') as json_file:
        json.dump(feature_dict,json_file)
        json_file.write('\n')

ean_list = []
with open('Product features to do.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for i, row in enumerate(reader):
        if i >= 1:
            ean_list.append(row[6])

if __name__=='__main__':
    file_name = "mecateo_data.json"
    # ean = '7310617252000'
    # ean = '4007368118817'
    # ean = '4007368118831'
    last_row = getLastAppended(file_name)
    if last_row is None:
        for ean in ean_list:
            features_dict = {}
            main(ean,features_dict)
    else:
        print(last_row)
        last_ean = last_row['ean']
        index = ean_list.index(last_ean) +1 
        for i in range(index, len(ean_list)):
            features_dict = {}
            print(ean_list[i])
            main(ean_list[i],features_dict)




