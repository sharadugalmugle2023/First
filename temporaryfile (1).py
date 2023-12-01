import time
import csv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome WebDriver
# ser_obj = Service("/home/user/Desktop/Dataeaze/Agri-POC/chrome-driver")
"/home/user/selenium-automation/chromedriver_linux64"
ser_obj = Service("/home/user/selenium-automation/chromedriver_linux64")
driver = webdriver.Chrome(service=ser_obj)
driver.maximize_window()

# Open the website
driver.get('https://agmarknet.gov.in')
# Wait for the table to load (you can adjust the wait time as needed)
wait = WebDriverWait(driver, 10)

#
# price_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlArrivalPrice']")
# price_dropdown = Select(price_dropdown)
# price_dropdown.select_by_visible_text("Both")
# time.sleep(2)

commodity_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlCommodity']")
commodity_select = Select(commodity_dropdown)
commodity_select.select_by_visible_text("Tomato")

state_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlState']")
state_dropdown = Select(state_dropdown)
state_dropdown.select_by_visible_text("Maharashtra")
time.sleep(2)

district_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlDistrict']")
district_dropdown = Select(district_dropdown)
district_dropdown.select_by_visible_text("Pune")
time.sleep(2)

market_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlMarket']")
market_dropdown = Select(market_dropdown)
market_dropdown.select_by_visible_text("Pune")
time.sleep(2)

# <---------->

from_date_dropdown = driver.find_element(By.XPATH, "//input[@id='txtDate']")
from_date_dropdown.clear()
date_string = "1-Jan-2022"
from_date_dropdown.send_keys(date_string + Keys.RETURN)
time.sleep(2)

to_date_dropdown = driver.find_element(By.XPATH, "//input[@id='txtDateTo']")
to_date_dropdown.clear()
date_string = "28-Feb-2022"
to_date_dropdown.send_keys(date_string + Keys.RETURN)
time.sleep(2)
# <----------->
go_button = driver.find_element(By.XPATH, "//input[@id='btnGo']")
go_button.click()

# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphBody_GridPriceData"]/tbody')))


# Function to wait for the presence of the table element using a custom wait condition
def wait_for_table_presence():
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData')))
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cphBody_GridPriceData"]/tbody/tr')))
    except TimeoutException:
        print("Timeout waiting for the table to be present.")
        # Handle the exception or retry if needed

# Wait for the table to be present on the page
wait_for_table_presence()


# Function to extract data from the current page and append it to the 'data_rows' list
def extract_data_from_current_page():
    # Scroll to the bottom of the page to ensure all data is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the data to load (you can adjust the wait time as needed)

    # Find all the rows in the table
    rows = driver.find_elements(By.XPATH, '//*[@id="cphBody_GridPriceData"]/tbody/tr')
    # for row in rows:
    for row in range(0, len(rows)-1):
        cells = rows[row].find_elements(By.XPATH, "./td")
        row_data = [cell.text for cell in cells]
        if row_data:
            data_rows.append(row_data)
            print(row_data)
        else:
            print("No data found for row:", row)

        # try:
        #     cells = rows[row].find_elements(By.XPATH, "./td")
        #     row_data = [cell.text for cell in cells]
        #     if row_data:
        #         data_rows.append(row_data)
        # except EC.StaleElementReferenceException:
        #     # If the element becomes stale, re-locate the rows and cells
        #     # rows = driver.find_elements(By.XPATH, '//*[@id="cphBody_GridPriceData"]/tbody/tr')
        #     cells = rows[row].find_elements(By.XPATH, "./td")
        #     row_data = [cell.text for cell in cells]
        #     if row_data:
        #         data_rows.append(row_data)

# Create a list to store the data from all pages
data_rows = []

# Loop through each page and extract data
while True:
    extract_data_from_current_page()

    # Find the next button (if it exists)
    try:
        next_button = driver.find_element(By.XPATH, '//input[@alt=">"]')
        if next_button.get_attribute('disabled') == 'true':
            # If the next button is disabled, it means there are no more pages, so break the loop
            break

        # Click the next button to go to the next page
        next_button.click()
        wait.until(EC.staleness_of(next_button))  # Wait for the next page to load

    except EC.NoSuchElementException:
        # If the next button is not found, it means we are on the last page, so break the loop
        break

print("Data collected successfully from all pages!")

# Create a CSV file to store the data
with open('agricultural_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)     #//table[@id='cphBody_GridViewBoth']/tbody/tr/th
    # Write the column headers    //table[@id='cphBody_GridViewBoth']/tbody/tr/th
    # column_headers = driver.find_elements(By.XPATH, '//*[@id="cphBody_GridPriceData"]/tbody/tr/th')
    column_headers = driver.find_elements(By.XPATH,"//table[@id='cphBody_GridViewBoth']/tbody/tr/th" )
    header_text = [header.text for header in column_headers]
    csvwriter.writerow(header_text)

    # Write the table data from all pages
    csvwriter.writerows(data_rows)

print("Data saved to CSV successfully!")
input("Enter a value to stop the execution...")
driver.quit()
