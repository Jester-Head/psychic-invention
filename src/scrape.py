
import time
from random import randint

import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os



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

    df = pd.DataFrame(list(zip(topic,author,views,replies)),columns=['topic','author','views','replies'])
    
    df['class'] = wow_class.text 
    return df

def get_replies(driver,url,class_name,count=1):
    # comment=[]
    with driver:
        driver.get(url)
    #     for reply in range(1,int(count)):
    #         selector = f'#post_{reply} .cooked'
    #         comment.append(driver.find_element(By.CSS_SELECTOR,selector).text)
            
            # comments = [com.text for com in comments]
            # df = pd.DataFrame(columns=['comment'])
            # df['comment'][reply] = comment.text
            
        comments = driver.find_elements(By.CSS_SELECTOR,'.cooked > p')
        comments = [com.text for com in comments]
        time.sleep(randint(1,5))
        dates = driver.find_elements(By.CSS_SELECTOR,'.post-info.post-date > a > span')
        dates = [date.get_attribute('title') for date in dates]
        df = pd.DataFrame(list(zip(comments, dates)),
            columns =['comment', 'date'])        
        df['class'] = class_name
    return df

def get_links(driver,url):
    with driver:
        driver.get(url)
        time.sleep(randint(1,5))
        link = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix > span > a')
    class_links = [l.get_attribute('href') for l in link]
    return class_links

def check_file(class_name):
    filename = 'data\\'+ class_name +'.csv'
    if not os.path.exists(filename):
        with open(filename, 'w',encoding='utf-8') as f:
            f.writelines(['comment,date,class\n'])
    else:
        with open (filename,'r+',encoding='utf-8') as f:
            
            if str(f.readline())=='':
                f.writelines(['comment,date,class\n'])
    return filename
    
def scrape_class(driver,links,class_name,count=1):
    filename = check_file(class_name)
    for link in links:
        time.sleep(randint(1,5))
        df = get_replies(driver=driver,url=link,class_name=class_name,count=count)
        df.to_csv(filename,mode='a',index=False,header=False)
        
def get_reply_count(driver,url):
    
    with driver:
        driver.get(url)
        time.sleep(randint(1,5))
        count = driver.find_element(By.CSS_SELECTOR,'.replies>span').text

    return count
               
def avoid_detection():
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
    return driver
        
    


if __name__== "__main__":
    driver = avoid_detection()
    # Add Evoker later
    classes = {'Death Knight':'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175','Demon Hunter':'https://us.forums.blizzard.com/en/wow/c/classes/demon-hunter/176','Druid':'https://us.forums.blizzard.com/en/wow/c/classes/druid/177',
               'Hunter':'https://us.forums.blizzard.com/en/wow/c/classes/hunter/178','Mage':'https://us.forums.blizzard.com/en/wow/c/classes/mage/179','Monk':'https://us.forums.blizzard.com/en/wow/c/classes/monk/180',
               'Paladin':'https://us.forums.blizzard.com/en/wow/c/classes/paladin/181','Priest':'https://us.forums.blizzard.com/en/wow/c/classes/priest/182','Rogue':'https://us.forums.blizzard.com/en/wow/c/classes/rogue/183',
               'Shaman':'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184','Warlock':'https://us.forums.blizzard.com/en/wow/c/classes/warlock/185','Warrior':'https://us.forums.blizzard.com/en/wow/c/classes/warrior/186'}
    # classes = {'Death Knight':'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175'}
    for name in classes:
        url = classes.get(name)
        links = get_links(driver,url)
        scrape_class(driver=driver,links=links,class_name=name)
        time.sleep(randint(1,5))
    
    # url = 'https://us.forums.blizzard.com/en/wow/t/best-dk-names-thread-the-good-the-great-and-the-punny/698565'
    # count = get_reply_count(driver=driver,url=url)
    # # selector = f'#post_{count} > div > div.topic-body.clearfix > div.regular.contents > div'
    # # print(selector)
    # # df = get_replies(driver=driver,url=url,class_name='Death Knight',count=count)
    # print(df)

    driver.quit()
   
    
    
