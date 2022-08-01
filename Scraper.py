import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

initial_start = True


def delay():
    time.sleep(random.randint(2, 3))


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.get('https://www.ebay-kleinanzeigen.de/m-einloggen.html')
    print('Press enter, when logged in ')
    input()

    # search = input()
    search = 'iphone-13'
    # kriterien = input()
    filter_in_list = 'neu, keine kratzer, keine risse'.split(', ')
    filter_out_list = 'suche, kleine risse, kleine kratzer, case, hülle, tausch'.split(', ')

    all_items = []
    all_ids = []
    page_urls = []

    for page in range(1, 50):
        driver.get('https://www.ebay-kleinanzeigen.de/s-seite:' + str(page) + '/' + str(search) + '/k0')

        table = driver.find_element(By.XPATH, '//*[@id="srchrslt-adtable"]')
        items = table.find_elements(By.TAG_NAME, 'li')
        for item in items:
            if item.get_attribute('class') == 'ad-listitem lazyload-item   ':

                anzeigen_id = item.find_element(By.TAG_NAME, 'article').get_attribute('data-adid')

                if anzeigen_id not in all_ids:
                    all_ids.append(anzeigen_id)

                    page_urls.append(item.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        for url in page_urls:
            message = True
            driver.get(url)

            if initial_start:
                driver.find_element(By.XPATH, '//*[@id="vap-ovrly-secure"]/a').click()
                initial_start = False

            description = driver.find_element(By.ID, 'viewad-description-text').text
            for filter_in in filter_in_list:
                if filter_in.lower() in description.lower():
                    message = True
            for filter_out in filter_out_list:
                if filter_out.lower() in description.lower():
                    message = False

            if message:
                driver.find_element(By.XPATH, '//*[@id="viewad-contact-form"]/fieldset/div[1]/div/textarea').send_keys("test")
                # driver.find_element(By.XPATH, '//*[@id="viewad-contact-form"]/fieldset/div[4]/button').click()
                print(url)
                delay()
                delay()

        page_urls = []
