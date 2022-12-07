
import os
import time
import uuid
from random import randint

import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from reretry import retry


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
    driver.implicitly_wait(30)
    return driver


def check_exists_by_css(driver, selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True


def get_all_comments(driver, url, class_name='default', count=1):
    '''Iterates through list of ids and extracts comment data'''
    comment = []
    date = []
    post_count = get_id(driver=driver, url=url)
    likes = []
    ids = []
    topic=[]

    with driver:
        driver.get(url)
        html = driver.find_element(By.TAG_NAME, 'html')
        title = driver.find_element(By.CSS_SELECTOR,'.fancy-title').text
        wait = WebDriverWait(driver,30)
        for i in range(1,int(post_count)):
            try:
                # generate comment id
                ids.append(str(uuid.uuid4().hex))
                # post title for each comment to help with joins later
                topic.append(title)

                # comment_selector = f'#post_{i} div > div.topic-body.clearfix > div.regular.contents > div.cooked > p'
                comment_selector = f'#post_{i} .cooked > p'
                date_selector = f'#post_{i} .relative-date'
                like_selector = f'#post_{i} .btn-text'
                post_string = f'#post_{i}'

                element = driver.find_element(By.CSS_SELECTOR,post_string)
                time.sleep(0.2)
                driver.execute_script(
                    'arguments[0].scrollIntoView(true);', element)
                time.sleep(0.4)
                # comment.append(element.find_element(
                #     By.CSS_SELECTOR, comment_selector).text)
                comment.append(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,comment_selector))).text)
                date.append(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,date_selector))).get_attribute('title'))

                try :
                    likes.append(element.find_element(
                    By.CSS_SELECTOR, like_selector).text)
                except NoSuchElementException:
                    likes.append('0')
                    continue
            except (StaleElementReferenceException,NoSuchElementException):
                exception_data(topic=topic,post_id=post_string)
                time.sleep(10)
                pass


    df = pd.DataFrame(data=list(zip(ids,topic, comment, likes, date)), columns=[
                      'id', 'topic','comment', 'likes', 'date'])

    return df


# def get_all_comments(driver, url, class_name='default', count=1):
#     '''Iterates through list of ids and extracts comment data'''

#     post_count = get_id(driver=driver, url=url)
#     topic = get_topic(driver=driver, url=url)
#     comments = []
#     dates = []
#     like_count = []
#     comment_ids = []
#     comment_id = ''
#     with driver:
#         driver.get(url)
#         for i in range(1, int(post_count)+1):
#             try:
#                 comment_id, comment, likes, date = get_comment(
#                     driver, url, class_name='default', count=i)
                
#                 comment_ids.append(comment_id)
#                 comments.append(comment)
#                 like_count.append(likes)
#                 dates.append(date)
#             except:
#                 exception_data(topic=topic, post_id=comment_id)
#                 time.sleep(10)
#                 pass
                
#     df = pd.DataFrame(data=list(zip(comment_ids,topic,comments, like_count, dates)), columns=[
#                       'id','topic','comment', 'likes', 'date'])
#     df['topic'] = topic

#     return df


def get_topic(driver, url):
    wait = WebDriverWait(driver, 10)
    topic_selector = '.fancy-title'
    topic = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, topic_selector))).text
    return topic


# # # @retry((StaleElementReferenceException, NoSuchElementException), tries=3, delay = 30)
# def get_comment(driver, url, class_name='default', count=1):
#     comment = ''
#     date = ''
#     likes = ''
#     topic = ''
#     # comment_id = str(uuid.uuid4().hex)
#     comment_id = ''
#     wait = WebDriverWait(driver, 30)
    
#     try:
#         comment_selector = f'#post_{count} .cooked > p'
#         date_selector = f'#post_{count} .relative-date'
#         like_selector = f'#post_{count} .btn-text'
#         post_string = f'#post_{count}'

#         element = driver.find_element(By.CSS_SELECTOR, post_string)
#         driver.execute_script(
#             'arguments[0].scrollIntoView(true);', element)
#         time.sleep(0.4)

#         # comment.append(wait.until(EC.visibility_of_element_located(
#         #     (By.CSS_SELECTOR, comment_selector))).text)
#         # date.append(wait.until(EC.visibility_of_element_located(
#         #     (By.CSS_SELECTOR, date_selector))).get_attribute('title'))
#         # try:
#         #     likes.append(element.find_element(
#         #         By.CSS_SELECTOR, like_selector).text)
#         # except NoSuchElementException:
#         #     likes.append('0')
        
#         comment  = wait.until(EC.visibility_of_element_located(
#             (By.CSS_SELECTOR, comment_selector))).text
#         date = wait.until(EC.visibility_of_element_located(
#             (By.CSS_SELECTOR, date_selector))).get_attribute('title')
#         comment_id  = wait.until(EC.visibility_of_element_located(
#             (By.CSS_SELECTOR, post_string))).get_attribute('data-post-id')
#         try:
#             likes = element.find_element(
#                 By.CSS_SELECTOR, like_selector).text
#         except NoSuchElementException:
#             likes = '0'
#     except (StaleElementReferenceException, NoSuchElementException):
#         # exception_data(topic=topic, post_id=post_string)
#         print(post_string)
#         return comment_id, comment, likes, date

#     # finally:   
#     #     return comment_id, comment, likes, date
#     return comment_id, comment, likes, date


def exception_data(topic, post_id):
    error_dict = {'topic': topic, 'id': post_id}
    pd.DataFrame(error_dict).to_csv(
        'logs', mode='a', index=False, header=False)


def get_links(driver, url):
    '''Returns list of links for top post in the quarter'''
    with driver:
        driver.get(url)
        SCROLL_PAUSE_TIME = 0.75

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


def check_stats_file(class_name):
    filename = 'data\\' + class_name + 'Stats.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(['id,', 'topic,', 'date,', 'reply_count,',
                         'views,', 'users,', 'likes,', 'links\n'])
    else:
        with open(filename, 'r+', encoding='utf-8') as f:

            if str(f.readline()) == '':
                f.writelines(
                    ['id,', 'topic,', 'date,', 'reply_count,', 'views,', 'users,', 'likes,', 'links\n'])
    return filename


def check_comment_file(class_name):
    filename = 'data\\' + class_name + '.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(['id,', 'topic,', 'comment,', 'likes,', 'date\n'])
    else:
        with open(filename, 'r+', encoding='utf-8') as f:

            if str(f.readline()) == '':
                f.writelines(['id,', 'topic,', 'comment,', 'likes,', 'date\n'])
    return filename


def scrape_class_forums(driver, links, class_name):
    '''Get's replies from every link on first page in forum and saves to csv file'''
    comments_file = check_comment_file(class_name)
    stats_file = check_stats_file(class_name)
    for link in links:
        time.sleep(4)
        # get stats
        dfs = pd.DataFrame(data=class_stats(
            driver=driver, url=link, class_name=class_name), index=[0])
        # append to file
        dfs.to_csv(stats_file, mode='a', index=False, header=False)

        time.sleep(1)
        # get comments
        dfc = get_all_comments(driver=driver, url=link,
                          class_name=class_name)
        # append to file
        dfc.to_csv(comments_file, mode='a', index=False, header=False)


def get_id(driver, url):
    '''Scrolls page to get every post id.Returns list of ids'''
    with driver:
        driver.get(url)
        post_id = driver.find_element(
            By.CSS_SELECTOR, '.timeline-replies').text
        post_id = str.split(post_id)
    return post_id[2]


def class_stats(driver, url, class_name):
    # filename = check_stats_file(class_name)
    topic = ''
    date_created = ''
    reply_count = ''
    views = ''
    users = ''
    likes = ''
    links = ''
    topic_selector = '.fancy-title'
    date_selector = '.relative-date'
    reply_selector = '.replies .number'
    views_selector = '.views>span'
    users_selector = '.users .number'
    likes_selector = '.likes .number'
    links_selector = '.links .number'
    post_string = f'#post_1'
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    time.sleep(2)
    try:
        topic = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, topic_selector))).text
        topic_id  = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, post_string))).get_attribute('data-topic-id')
        date_created = driver.find_element(
            By.CSS_SELECTOR, date_selector).get_attribute('title')
    except NoSuchElementException:
        exception_data(topic, 0)

    try:
        if check_exists_by_css(driver, reply_selector):
            reply_count = driver.find_element(
                By.CSS_SELECTOR, reply_selector).text
        else:
            reply_count = '0'
        if check_exists_by_css(driver, views_selector):
            views = driver.find_element(By.CSS_SELECTOR, views_selector).text
        else:
            views = '0'
        if check_exists_by_css(driver, users_selector):
            users = driver.find_element(By.CSS_SELECTOR, users_selector).text
        else:
            users = '0'
        if check_exists_by_css(driver, likes_selector):
            likes = driver.find_element(By.CSS_SELECTOR, likes_selector).text
        else:
            likes = '0'
        if check_exists_by_css(driver, links_selector):
            links = driver.find_element(By.CSS_SELECTOR, links_selector).text
        else:
            links = '0'
    except:
        StaleElementReferenceException

    # df = pd.DataFrame(list(zip(topic,date_created,reply_count,views,users,likes,links)))

    # df.to_csv(filename,mode='a',index=False,header=False)
    stats = {'id': topic_id, 'topic': topic, 'date_created': date_created, 'reply_count': reply_count,
             'views': views, 'users': users, 'likes': likes, 'links': links}

    return stats


def test_func(driver, url):
    driver.get(url)
    # driver.find_element(By.TAG_NAME,'html').send_keys(Keys.END)
    # element = driver.find_element(By.CSS_SELECTOR,'.post-stream')
    # post_id = driver.find_elements(By.XPATH, './/*[contains(@id, "post")]')
    # post_id = driver.find_element(By.CSS_SELECTOR,'.timeline-replies').text
    # post_id =str.split(post_id)
    # post_id = [p.get_attribute('id') for p in post_id]
    # post_id = get_id(url)
    # print(post_id[2])
    driver.quit()


if __name__ == "__main__":
    #     # TODO change tie to UTC 0 before scraping
    driver = avoid_detection()
#     # classes = {'Death Knight': 'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175/l/top?period=quarterly', 'Demon Hunter': 'https://us.forums.blizzard.com/en/wow/c/classes/demon-hunter/176/l/top?period=quarterly', 'Druid': 'https://us.forums.blizzard.com/en/wow/c/classes/druid/177/l/top?period=quarterly', 'Evoker': 'https://us.forums.blizzard.com/en/wow/c/classes/evoker/275/l/top?period=quarterly',
#     #            'Hunter': 'https://us.forums.blizzard.com/en/wow/c/classes/hunter/178/l/top?period=quarterly', 'Mage': 'https://us.forums.blizzard.com/en/wow/c/classes/mage/179/l/top?period=quarterly', 'Monk': 'https://us.forums.blizzard.com/en/wow/c/classes/monk/180/l/top?period=quarterly',
#     #            'Paladin': 'https://us.forums.blizzard.com/en/wow/c/classes/paladin/181/l/top?period=quarterly', 'Priest': 'https://us.forums.blizzard.com/en/wow/c/classes/priest/182/l/top?period=quarterly', 'Rogue': 'https://us.forums.blizzard.com/en/wow/c/classes/rogue/183/l/top?period=quarterly',
#     #            'Shaman': 'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184/l/top?period=quarterly', 'Warlock': 'https://us.forums.blizzard.com/en/wow/c/classes/warlock/185/l/top?period=quarterly', 'Warrior': 'https://us.forums.blizzard.com/en/wow/c/classes/warrior/186/l/top?period=quarterly'}
#     # classes = {'Rogue': 'https://us.forums.blizzard.com/en/wow/c/classes/rogue/183/l/top?period=quarterly','Shaman': 'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184/l/top?period=quarterly'}
    classes = {
        'Shaman': 'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184/l/top?period=quarterly'}
    for name in classes:
        url = classes.get(name)
        links = get_links(driver, url)
        scrape_class_forums(driver=driver, links=links, class_name=name)
        time.sleep(5)

    # url = 'https://us.forums.blizzard.com/en/wow/t/still-waiting-on-that-frostmournebotfp-mog-blizz/1396408'

    # test_func(driver,url)

    # driver.quit()
