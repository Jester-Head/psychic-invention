
import time
from random import randint

import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# import no_detect


def get_class_page(driver,url):
    with driver:
        driver.get(url)
        time.sleep(randint(1,5))
        
        author = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'td.creator')))
        author = [c.text for c in author]
        
        time.sleep(randint(1,5))

        topic = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix')
        topic = [t.text for t in topic]
        
        time.sleep(randint(1,5))


        replies = driver.find_elements(By.CSS_SELECTOR,'td.num.posts-map.posts.topic-list-data > button > span')
        replies = [r.text for r in replies]
        
        time.sleep(randint(1,5))


        views = driver.find_elements(By.CSS_SELECTOR,'td.num.views > span')
        views = [v.text for v in views]
        
        time.sleep(randint(1,5))

        link = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix > span > a')
        link = [l.get_attribute('href') for l in link]
        
        time.sleep(2)
        wow_class = driver.find_element(By.CSS_SELECTOR,'#ember49-header .category-name')
    # driver.quit()

    df = pd.DataFrame(list(zip(topic,author,views,replies)),columns=['topic','author','views','replies'])
    
    df['class'] = wow_class.text 
    return df

def get_replies(driver,url):
    with driver:
        driver.get(url)
        class_forum = 'Demon Hunter'
        comments = driver.find_elements(By.XPATH,'.//*[contains(concat( " ", @class, " " ), concat( " ", "cooked", " " ))]')
        comments = [com.text for com in comments]
        df = pd.DataFrame(data=comments,columns=['comments'])
        df['class'] = class_forum

    return df

def get_links(driver,url):
    with driver:
        driver.get(url)
        time.sleep(randint(1,5))
        link = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix > span > a')
    class_links = [l.get_attribute('href') for l in link]
        # class_links = [item.get_attribute("href") for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"td.main-link.clearfix > span > a")))]

    return class_links
    


if __name__== "__main__":
    options = uc.ChromeOptions()

    # setting profile
    options.user_data_dir = "c:\\temp\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=c:\\temp\\profile2')

    #Change Browser Options
    options.add_argument('proxy-server=106.122.8.54:3128')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')


    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = uc.Chrome(options=options)
    

    url = 'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175'
    # url = 'https://us.forums.blizzard.com/en/wow/t/please-fix-momentum-before-launch-day/1381495'
#  
    # dfc = get_replies(driver,url)
    # dfc = get_class_page(driver=driver,url=url)
    # print(dfc)
    # dfc.to_csv('class_threads',index=False)
    # dfc.to_csv('class_page',index=False)
    links = get_links(driver,url)
    # print(links)
    post = get_replies(driver,links[0])
    driver.quit()
    print(post)

