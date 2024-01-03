from chrome_setup import chrome_setup
from selenium.webdriver.common.by import By
from time import sleep

driver = chrome_setup()
driver.get('https://www.linkedin.com')

username = driver.find_element(By.NAME, value='session_key')
password = driver.find_element(By.NAME, value='session_password')



# driver.quit()

