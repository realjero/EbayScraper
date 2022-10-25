import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

initial_start = True

input_text = "test"


def delay():
    time.sleep(random.randint(3, 4))


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.get('https://www.ebay-kleinanzeigen.de/m-einloggen.html')
    print('Press enter, when logged in ')
    input()

    print('for automated search, enter item and press enter.')
    search = input().replace(' ', '-')

    print('enter from price')
    from1 = input()

    print('enter to price')
    to = input()

    print("example ('neu, keine kratzer, keine risse')")
    print('add words to whitelist (", " for separated words)')
    whitelist = input().split(', ')

    print("example ('suche, kleine risse, kleine kratzer, case, hülle, tausch')")
    print('add words to blacklist (", " for separated words)')
    blacklist = input().split(', ')

    file = open('ids.log', 'r')
    all_ids = file.read().splitlines()
    file.close()

    page_urls = []

    file = open('ids.log', 'a')

    for page in range(1, 50):
        driver.get('https://www.ebay-kleinanzeigen.de/s-preis:' + str(from1) + ':' + str(to) + '/s-seite:' + str(page) + '/' + str(search) + '/k0')

        items = driver.find_element(By.XPATH, '//*[@id="srchrslt-adtable"]').find_elements(By.TAG_NAME, 'li')

        for item in items:
            if item.get_attribute('class') == 'ad-listitem lazyload-item   ':

                bay_id = item.find_element(By.TAG_NAME, 'article').get_attribute('data-adid')

                if bay_id not in all_ids:
                    all_ids.append(bay_id)
                    file.write(bay_id + '\n')

                    page_urls.append(item.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        for url in page_urls:
            message = True
            driver.get(url)
            delay()

            if initial_start:
                driver.find_element(By.XPATH, '//*[@id="vap-ovrly-secure"]/a').click()
                initial_start = False

            description = driver.find_element(By.ID, 'viewad-description-text').text

            for filter_in in whitelist:
                if filter_in.lower() in description.lower():
                    message = True

            for filter_out in blacklist:
                if filter_out.lower() in description.lower():
                    message = False

            if message:
                driver.find_element(By.XPATH, '//*[@id="viewad-contact-form"]/fieldset/div[1]/div/textarea').send_keys(input_text)
                driver.find_element(By.XPATH, '//*[@id="viewad-contact-form"]/fieldset/div[4]/button').click()
                delay()

        page_urls = []