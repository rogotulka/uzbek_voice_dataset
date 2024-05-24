import random

import requests
from selenium import webdriver
import time
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By


URL_ROOT = "https://sharh.commeta.uz/"

sub_dirs = ['click']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = webdriver.Chrome(options=chrome_options)

from selenium.webdriver.chrome.options import Options

driver.get(URL_ROOT + sub_dirs[0])

time.sleep(5)

driver.execute_script("window.scrollTo(0, 2500)")

time.sleep(5)

element = driver.find_element(By.XPATH, "//span[contains(text(), 'Yana yuklash')]")

ActionChains(driver).click(element).perform()

time.sleep(10)

