from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

# Input the an address, neighborhood, city, or ZIP code you are interested in
print()
address_input = input('Enter an address, neighborhood, city, or ZIP code ...:  ')

driver = webdriver.Chrome("copy your chrome driver directory here ...")

driver.maximize_window()
sleep(0.5)

driver.get('https://www.zillow.com/')
sleep(0.5)

search_input = driver.find_element_by_xpath('//input[@id = "search-box-input"]')
search_input.send_keys('')
sleep(0.5)

driver.find_element_by_xpath('//button[@id = "search-icon"]').click()
sleep(0.5)

driver.find_element_by_xpath('//button[text()="For rent"]').click()
sleep(0.5)

search_input = driver.find_element_by_xpath('//input[@placeholder = "Address, neighborhood, or ZIP"]')
search_input.send_keys(Keys.CONTROL + "a")
search_input.send_keys(Keys.DELETE)
search_input.send_keys(address_input)
sleep(0.5)
search_input.submit()
sleep(0.5)


is_next_page = True

current_page_url = ''

prices_info = []
addresses = []

print()
print('Start scraping...')
while(is_next_page):
    prices_info_temp = driver.find_elements_by_xpath('//div[@class = "list-card-heading"]')
    prices_info_temp = [price_info.text for price_info in prices_info_temp]
    prices_info = prices_info + prices_info_temp
    

    addresses_temp = driver.find_elements_by_xpath('//address[@class = "list-card-addr"]')
    addresses_temp = [address.text for address in addresses_temp]
    addresses = addresses + addresses_temp

    next_page = driver.find_element_by_xpath('//a[@title = "Next page"]')

    next_page_url = next_page.get_attribute('href') 
    if next_page_url == current_page_url:
        is_next_page = False
    else:
        next_page.click()
        current_page_url = next_page_url
    sleep(3)
print()
print('Finished scraping.')
driver.quit()
apartment_info = list(zip(addresses, prices_info))
columns_name = ['Addresses', 'Prices']
apartment_dataset = pd.DataFrame(columns = columns_name, data = apartment_info)
apartment_dataset.to_csv('apartment_dataset.csv', index = False)
print()
print('Data saved.')












