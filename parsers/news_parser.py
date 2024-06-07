# import random

# import requests
# from selenium import webdriver
# import time
# from selenium.webdriver import ActionChains

# from selenium.webdriver.common.by import By


# URL_ROOT = "https://sharh.commeta.uz/"

# sub_dirs = ['click']

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--enable-logging')
# chrome_options.add_argument('--log-level=0')
# chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
# driver = webdriver.Chrome(options=chrome_options)

# from selenium.webdriver.chrome.options import Options

# driver.get(URL_ROOT + sub_dirs[0])

# time.sleep(5)

# driver.execute_script("window.scrollTo(0, 2500)")

# time.sleep(5)

# element = driver.find_element(By.XPATH, "//span[contains(text(), 'Yana yuklash')]")

# ActionChains(driver).click(element).perform()

# time.sleep(10)


import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка Chrome Driver
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Для запуска в фоновом режиме, без GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Инициализация WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = webdriver.Chrome(options=chrome_options)

# try:
    # class="p-3 md:p-4 max-md:pb-2 flex md:justify-between items-start w-full gap-4 cursor-pointer"
driver.get("https://sharh.commeta.uz/ru/category/finance")
# driver.get("https://sharh.commeta.uz/ru/click")
time.sleep(7)
while True:
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bg-white.company-card.rounded-xl.transition-300.border-b.border-divide\\/40'))
    # )
    elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
    if not elements:
        break
    for element in elements:
        ActionChains(driver).click(element).perform()
        time.sleep(3)

# categories = driver.find_elements(By.XPATH, '//*[@id="__nuxt"]/div/div[2]/div[2]/div/section/main/section/div/div[2]/div[1]/div[1]/div[1]/div')
categories = driver.find_elements(By.CSS_SELECTOR, 'div.bg-white.company-card.rounded-xl.transition-300.border-b.border-divide\\/40')
# reviews = driver.find_elements(By.XPATH, "//div[@data-v-792071f1]/span[@data-v-792071f1]")
print(categories)

# p-3 md:p-4 max-md:pb-2 flex md:justify-between items-start w-full gap-4 cursor-pointer
time.sleep(300)
categories_list = []
for c in categories:
    
    ActionChains(driver).click(c).perform()
    time.sleep(1)
    print(driver.current_url)
    categories_list.append(driver.current_url.split('/')[-1])
    driver.back()


for c_name in categories:
    # Set to store unique data
    unique_data = set()

    while True:
        time.sleep(5)

        # Скроллинг страницы
        driver.execute_script("window.scrollTo(0, 5000)")

        time.sleep(5)

        # Получение отзывов и никнеймов
        reviews = driver.find_elements(By.XPATH, "//div[@data-v-792071f1]/span[@data-v-792071f1]")
        nicknames = driver.find_elements(By.XPATH, "//h3[@class='text-base font-semibold leading-130 text-blue-800 duration-300 line-clamp-1 hover:text-blue']")

        # Сохранение уникальных данных в списки
        for review, nickname in zip(reviews, nicknames):
            review_text = review.text
            nickname_text = nickname.text
            if (nickname_text, review_text) not in unique_data:
                unique_data.add((nickname_text, review_text))

        # Сохранение данных в файле CSV
        with open('reviews.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['Nickname', 'Review'])  # Writing column headers
            for nickname_text, review_text in unique_data:
                writer.writerow([nickname_text, review_text])

        # Проверка наличия кнопки "Yana yuklash" для загрузки дополнительных данных
        elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
        if not elements:
            break

        # Клик по кнопке "Загрузить ещё"
        for element in elements:
            ActionChains(driver).click(element).perform()

        time.sleep(2)

# finally:
#     # Закрытие браузера
#     driver.quit()





''' LAST UPDATE


import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys 

# Chrome options configuration
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the URL
    driver.get("https://sharh.commeta.uz/ru/category/finance")
    time.sleep(7)

    # Load additional content until no more elements found
    while True:
        elements = driver.find_elements(By.XPATH,
                                        "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
        if not elements:
            break
        for element in elements:
            ActionChains(driver).click(element).perform()
            time.sleep(3)


    # Extract categories
    categories = driver.find_elements(By.CSS_SELECTOR,
                                      'div.bg-white.company-card.rounded-xl.transition-300.border-b.border-divide\\/40')
    print(categories)

    # Wait for 5 minutes
    time.sleep(6)

    # Collect category URLs
    categories_list = []
    for category in categories:
        print(category)
        # ActionChains(driver).click(category).perform()
        category.send_keys(Keys.CONTROL + 't')
        time.sleep(1)

        print(driver.current_url)
        categories_list.append(driver.current_url.split('/')[-1])
        driver.back()
        driver.execute_script("window.scrollTo(0,5000);")
        time.sleep(3)  # Adjust the sleep time as needed to wait for the scroll

finally:
    # Close the browser
    driver.quit()


'''
