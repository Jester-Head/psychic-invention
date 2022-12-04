
import os
import time
from random import randint

import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def avoid_detection():
    options = uc.ChromeOptions()

    # setting profile
    options.user_data_dir = "c:\\temp\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=c:\\temp\\profile2')

    # Change Browser Options
    options.add_argument('proxy-server=106.122.8.54:3128')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')

    # just some options passing in to skip annoying popups
    options.add_argument(
        '--no-first-run --no-service-autorun --password-store=basic')
    driver = uc.Chrome(options=options)
    return driver


def get_replies(driver, url, class_name='default', count=1):
    '''Iterates through list of ids and extracts comment data'''
    comment = []
    date = []
    posts = get_id(driver=driver, url=url)
    likes = []
    with driver:
        driver.get(url)
        html = driver.find_element(By.TAG_NAME, 'html')
        for post in posts:
            try:

                comment_selector = f'#{post} div > div.topic-body.clearfix > div.regular.contents > div.cooked > p'
                date_selector = f'#{post} .relative-date'

                like_selector = f'#{post} .btn-text'

                element = driver.find_element(By.CSS_SELECTOR, f'#{post}')
                driver.execute_script(
                    'arguments[0].scrollIntoView(true);', element)
                time.sleep(0.4)
                comment.append(element.find_element(
                    By.CSS_SELECTOR, comment_selector).text)

                date.append(element.find_element(By.CSS_SELECTOR,
                            date_selector).get_attribute('title'))

                likes.append(element.find_element(
                    By.CSS_SELECTOR, like_selector).text)
            except:
                print(post)
                likes.append('0')
                continue

    df = pd.DataFrame(data=list(zip(posts, comment, likes, date)), columns=[
                      'post_id', 'comment', 'likes', 'date'])

    return df


def get_links(driver, url):
    '''Returns list of links for top post in the quarter'''
    with driver:
        driver.get(url)
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        class_links = driver.find_elements(
            By.CSS_SELECTOR, 'td.main-link.clearfix > span > a')
        class_links = [l.get_attribute('href') for l in class_links]
    return class_links


def check_file(class_name):
    filename = 'data\\' + class_name + '.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(['comment,date,class\n'])
    else:
        with open(filename, 'r+', encoding='utf-8') as f:

            if str(f.readline()) == '':
                f.writelines(['comment,date,class\n'])
    return filename


def scrape_class_forums(driver, links, class_name, count=1):
    '''Get's replies from every link on first page in forum and saves to csv file'''
    filename = check_file(class_name)
    for link in links:
        time.sleep(2)
        df = get_replies(driver=driver, url=link,
                         class_name=class_name, count=count)
        df.to_csv(filename, mode='a', index=False, header=False)


def get_id(driver, url):
    '''Scrolls page to get every post id.Returns list of ids'''
    with driver:
        driver.get(url)
        while True:
            previous_scrollY = driver.execute_script('return window.scrollY')
            driver.execute_script('window.scrollBy( 0, 230 )')
            time.sleep(0.4)
            if previous_scrollY == driver.execute_script('return window.scrollY'):
                post_id = driver.find_elements(
                    By.XPATH, './/*[contains(@id, "post")]')
                post_id = [p.get_attribute('id') for p in post_id]
                return post_id


def test_func(driver, url):
    links = get_links(driver, url)
    scrape_class_forums(driver=driver, links=links, class_name='Hunter')
    driver.quit()


if __name__ == "__main__":
    # TODO change tie to UTC 0 before scraping
    driver = avoid_detection()
    # classes = {'Death Knight':'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175/l/top?period=quarterly','Demon Hunter':'https://us.forums.blizzard.com/en/wow/c/classes/demon-hunter/176/l/top?period=quarterly','Druid':'https://us.forums.blizzard.com/en/wow/c/classes/druid/177/l/top?period=quarterly','Evoker':'https://us.forums.blizzard.com/en/wow/c/classes/evoker/275/l/top?period=quarterly'
    #            'Hunter':'https://us.forums.blizzard.com/en/wow/c/classes/hunter/178/l/top?period=quarterly','Mage':'https://us.forums.blizzard.com/en/wow/c/classes/mage/179/l/top?period=quarterly','Monk':'https://us.forums.blizzard.com/en/wow/c/classes/monk/180/l/top?period=quarterly',
    #            'Paladin':'https://us.forums.blizzard.com/en/wow/c/classes/paladin/181/l/top?period=quarterly','Priest':'https://us.forums.blizzard.com/en/wow/c/classes/priest/182/l/top?period=quarterly','Rogue':'https://us.forums.blizzard.com/en/wow/c/classes/rogue/183/l/top?period=quarterly',
    #            'Shaman':'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184/l/top?period=quarterly','Warlock':'https://us.forums.blizzard.com/en/wow/c/classes/warlock/185/l/top?period=quarterly','Warrior':'https://us.forums.blizzard.com/en/wow/c/classes/warrior/186/l/top?period=quarterly'}
    # classes = {'Death Knight':'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175/l/top?period=quarterly'}
    # for name in classes:
    #     url = classes.get(name)
    #     links = get_links(driver,url)
    #     scrape_class(driver=driver,links=links,class_name=name)
    #     time.sleep(randint(1,5))

    # url = 'https://us.forums.blizzard.com/en/wow/t/best-dk-names-thread-the-good-the-great-and-the-punny/698565'
    # url = 'https://us.forums.blizzard.com/en/wow/t/frostunholy-dk-looking-good-for-df/1399916'
    # url = 'https://us.forums.blizzard.com/en/wow/t/dks-trash-thnx-blizz/1428270'
    url = 'https://us.forums.blizzard.com/en/wow/c/classes/hunter/178/l/top?period=quarterly'
    test_func(driver=driver, url=url)

    # count = get_reply_count(driver=driver,url=url)
    # # selector = f'#post_{count} > div > div.topic-body.clearfix > div.regular.contents > div'
    # # print(selector)
    # # df = get_replies(driver=driver,url=url,class_name='Death Knight',count=count)
    # print(df)
    driver.quit()
