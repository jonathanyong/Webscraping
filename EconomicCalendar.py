import time
import selenium.webdriver as webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException,TimeoutException, NoSuchElementException
import pandas as pd

urls = ['https://www.investing.com/economic-calendar/']

options = Options()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

for url in urls:
    driver.get(url)
    site = requests.get(url)

    #step 1.1. Get the file base name
    file_base_name = url.split('/')[-2]
    print(f'Scraping {url}...')
    #step 1.2. Create Excel writer
    xlwriter = pd.ExcelWriter(file_base_name + '.xlsx')

    #step 2. Apply filter
    # open filters
    filter_tab = driver.find_element(By.ID,'filterStateAnchor') 
    try:
        filter_tab.click()
    except ElementNotInteractableException:
        pass
    time.sleep(2)
    # clear all country selections
    clear_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//a[starts-with(@onclick,'clearAll')]")))
    clear_tab.click()
    # choose Singapore
    singapore_option = driver.find_element(By.ID,'country36')
    singapore_option.click()
    # choose United States
    us_option = driver.find_element(By.ID,'country5')
    us_option.click()
    # choose importance 3
    importance_3 = driver.find_element(By.ID,'importance3')
    importance_3.click()
    # apply the filters and wait for the page to reload
    apply_filters = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,'ecSubmitButton')))
    apply_filters.click()
    #time.sleep(5)
    #Scroll page via js
    driver.execute_script("window.scrollBy(0,-1000)")
    time.sleep(1)
    
    #step 3. Change Timezone
    Timezone_tab = driver.find_element(By.CLASS_NAME,'dropDownArrowGray')
    Timezone_tab.click()
    time.sleep(1)
    Singapore_time = driver.find_element(By.XPATH,f'//li[@id="liTz113"]')
    Singapore_time.click()
    Timezone_tab.click()

    #step 4. Extract Data from each category
    categories = ['This Week', 'Next Week']
    for category in categories:
        print(f'Processing report: {category}')
        try:
            # select this week or next week calendar
            period_tab = driver.find_element(By.XPATH,f'//a[text()="{category}"]')
            try:
                period_tab.click()
            except ElementNotInteractableException:
                pass
            # delay execution for a table to load
            time.sleep(2)
            list_table = driver.find_element(By.ID,'economicCalendarData')
            # extract header from table
            header_row = []
            list_tag_header = list_table.find_elements(By.TAG_NAME,'thead')[0]
            header_date = ['Date']
            header_data = [th.text for th in list_tag_header.find_elements(By.TAG_NAME,'th')]
            header_row.append(header_date + header_data)
            header_row = [x for x in header_row[0] if x != '']
            print(header_row)
            # extract content from table
            content_row = []
            list_tag_body = list_table.find_element(By.TAG_NAME,'tbody')
            list_tag_tr = list_tag_body.find_elements(By.TAG_NAME,'tr')
            for tr in list_tag_tr:
                try:
                    list_tag_td = [td.text for td in tr.find_elements(By.TAG_NAME,'td')[0:7]]
                    if len(list_tag_td)==1:
                        list_tag_td_date = list_tag_td
                    else:
                        content_row.append(list_tag_td_date+list_tag_td)
                except:
                    print("No Td!")

            print(header_row)
            print(content_row)
                
            df = pd.DataFrame(content_row,columns=header_row)
            df.to_excel(xlwriter, sheet_name=category, index=False)

            print(df)
                    
        except (NoSuchElementException, TimeoutException):
            continue
            
    xlwriter.save()
    xlwriter.close()

driver.close()
