""" Module used to test and learn how to find web elements by CLASS_NAME and
    ID.  Also learn how to click buttons and enter text into an input field.
"""

from time import sleep
# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# create webdriver object
driver = webdriver.Firefox()

driver.get("https://earthquake.usgs.gov/earthquakes/search")

driver.find_element(by=By.ID, value="custom-mag").click()

element = driver.find_element(by=By.ID, value="minmagnitude")

# send keys
element.send_keys("1")

element = driver.find_element(by=By.ID, value="maxmagnitude")
element.send_keys("10")
element.send_keys(Keys.TAB)

driver.find_element(by=By.ID, value="basictime-custom").click()
element.send_keys(Keys.TAB)

element = driver.find_element(by=By.ID, value="starttime")
element.send_keys(Keys.CLEAR)
element.send_keys("2021-12-01 00:00:00")

driver.find_element(by=By.CLASS_NAME, value="toggle").click()

element = driver.find_element(by=By.ID, value="maxlatitude")
element.send_keys("35.261")
element.send_keys(Keys.TAB)

element = driver.find_element(by=By.ID, value="minlongitude")
element.send_keys("-83.485")
element.send_keys(Keys.TAB)

element = driver.find_element(by=By.ID, value="maxlongitude")
element.send_keys("-77.860")
element.send_keys(Keys.TAB)

element = driver.find_element(by=By.ID, value="minlatitude")
element.send_keys("31.977")
element.send_keys(Keys.TAB)

driver.find_element(by=By.ID, value="search-output").click()

driver.find_element(by=By.ID, value="output-format-geojson").click()
driver.find_element(by=By.ID, value="fdsn-submit").click()
sleep(5)
