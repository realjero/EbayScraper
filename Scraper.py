import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def delay():
    time.sleep(random.randint(2, 3))


if __name__ == '__main__':
    driver = uc.Chrome()

    # search = input()
    search = 'iphone-13'
    # kriterien = input()

    all_items = []
    all_ids = []
    page_urls = []

    for page in range(1, 50):
        driver.get('https://www.ebay-kleinanzeigen.de/s-seite:' + str(page) + '/' + str(search) + '/k0')
        delay()

        table = driver.find_element(By.XPATH, '//*[@id="srchrslt-adtable"]')
        items = table.find_elements(By.TAG_NAME, 'li')
        for item in items:
            if item.get_attribute('class') == 'ad-listitem lazyload-item   ':

                anzeigen_id = item.find_element(By.TAG_NAME, 'article').get_attribute('data-adid')

                if anzeigen_id not in all_ids:
                    all_ids.append(anzeigen_id)

                    page_urls.append(item.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        for url in page_urls:
            driver.get(url)
            delay()
            print(driver.find_element(By.ID, 'viewad-description-text').text)

        page_urls = []
