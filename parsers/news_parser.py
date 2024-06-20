import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

try:

    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Для запуска в фоновом режиме, без GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://sharh.commeta.uz/ru/category/finance")
    time.sleep(7)
    while True:
        elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
        if not elements:
            break
        for element in elements:
            ActionChains(driver).click(element).perform()
            time.sleep(3)

    categories = driver.find_elements(By.CSS_SELECTOR, 'span.font-semibold.leading-130.text-dark.break-all.line-clamp-1')

    for c in categories:
        c_name = c.text.lower()
        if c_name == 'universal bank':
            c_name = 'h4ei'
        if c_name == 'kapitalbank':
            c_name = 'kapital'
        if c_name == 'nbu':
            c_name = 'a4pw'
        if c_name == 'zte corporation':
            c_name = 'zte_corporation'

        c_name = c_name.replace(' ', '-')
        c_name = c_name.replace('‘', '')
        c_name = c_name.replace('.', '')
        c_name = c_name.replace('(', '')
        c_name = c_name.replace(')', '')
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://sharh.commeta.uz/ru/{c_name}")

        time.sleep(3)


        unique_data = set()

        while True:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 4500)")

            time.sleep(5)

            reviews = driver.find_elements(By.XPATH, "//div[@class='text-sm leading-130 text-dark word-break-break-word whitespace-pre-line']/span")
            nicknames = driver.find_elements(By.XPATH, "//h3[@class='text-base font-semibold leading-130 text-blue-800 duration-300 whitespace-nowrap overflow-hidden w-[200px] text-ellipsis line hover:text-blue']/a")

            for review, nickname in zip(reviews, nicknames):
                
                review_text = review.text
                nickname_text = nickname.text
                if (nickname_text, review_text) not in unique_data:
                    unique_data.add((nickname_text, review_text))

            elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
            if not elements:
                break

            for element in elements:
                ActionChains(driver).click(element).perform()

            unfold_comms = driver.find_elements(By.CSS_SELECTOR, "button[class='text-blue cursor-pointer ml-0.5']")
            if unfold_comms:
                for element in unfold_comms:
                    ActionChains(driver).click(element).perform()
                    
            time.sleep(2)

        # Сохранение данных в файле CSV
        with open(f'{c_name}_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['Nickname', 'Review'])
            for nickname_text, review_text in unique_data:
                writer.writerow([nickname_text, review_text])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()




''' LAST UPDATE

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

try:
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://sharh.commeta.uz/ru/category/finance")
    time.sleep(5)

    while True:
        elements = driver.find_elements(By.XPATH,
                                        "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
        if not elements:
            break
        for element in elements:
            ActionChains(driver).click(element).perform()
            time.sleep(3)

    categories = driver.find_elements(By.CSS_SELECTOR,
                                      'span.font-semibold.leading-130.text-dark.break-all.line-clamp-1')

    for c in categories:
        c_name = c.text.lower()
        if c_name == 'universal bank':
            c_name = 'h4ei'
        elif c_name == 'kapitalbank':
            c_name = 'kapital'
        elif c_name == 'nbu':
            c_name = 'a4pw'
        elif c_name == 'zte corporation':
            c_name = 'zte_corporation'

        c_name = c_name.replace(' ', '-')
        c_name = c_name.replace('‘', '')
        c_name = c_name.replace('.', '')
        c_name = c_name.replace('(', '')
        c_name = c_name.replace(')', '')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://sharh.commeta.uz/ru/{c_name}")
        time.sleep(3)

        while True:

            driver.execute_script("window.scrollTo(0, 4500)")
            time.sleep(3)

            elements = driver.find_elements(By.XPATH,
                                            "//span[contains(text(), 'Yana yuklash') or contains(text(), 'Загрузить еще') or contains(text(), 'Load more') or contains(text(), 'Яна юклаш')]")
            if not elements:
                break

            for element in elements:
                ActionChains(driver).click(element).perform()

            unfold_comms = driver.find_elements(By.CSS_SELECTOR, "button[class='text-blue cursor-pointer ml-0.5']")
            if unfold_comms:
                for element in unfold_comms:
                    ActionChains(driver).click(element).perform()

        time.sleep(5)

        reviews = driver.find_elements(By.XPATH,
                                       "//div[@class='text-sm leading-130 text-dark word-break-break-word whitespace-pre-line']/span")
        nicknames = driver.find_elements(By.XPATH,
                                         "//h3[@class='text-base font-semibold leading-130 text-blue-800 duration-300 whitespace-nowrap overflow-hidden max-sm:max-w-[200px] text-ellipsis line hover:text-blue']/a")

        with open(f'{c_name}_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            for review, nickname in zip(reviews, nicknames):
                writer.writerow([nickname.text, review.text])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()


'''
