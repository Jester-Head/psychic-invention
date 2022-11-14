
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
    driver.get(url)
    # time.sleep(randint(1,5))
    
    author = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'td.creator')))
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
    # driver.quit()

    df = pd.DataFrame(list(zip(topic,author,views,replies)),columns=['topic','author','views','replies'])
    return df

def get_replies(driver,url):
    with driver:
        driver.get(url)
        # comments = driver.find_elements(By.CSS_SELECTOR,'div.topic-body.clearfix.highlighted > div.regular.contents')
        # comments = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'class.post[itemprop="articleBody"]')))
        # comments = driver.find_elements(By.XPATH,'.//*[contains(concat( " ", @class, " " ), concat( " ", "post-stream", " " ))]')
        comments = driver.find_elements(By.XPATH,'.//*[contains(concat( " ", @class, " " ), concat( " ", "cooked", " " ))]')
        comments = [com.text for com in comments]
        # comments = comments[3:]
        # time.sleep(randint(1,5))
        # author = driver.find_elements(By.XPATH,'.//*[contains(concat( " ", @class, " " ), concat( " ", "character-name", " " ))]')
        # author = [a.text for a in author]
        
        # df = pd.DataFrame(list(zip(comments,author)),columns=['comments','author'])
        df = pd.DataFrame(comments,columns=['comments'])

    return df
    


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
    
    
    # service = Service('C:\chromedriver_win32\chromedriver')
    # driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver')
    url = 'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175'
    # url = 'https://us.forums.blizzard.com/en/wow/t/please-fix-momentum-before-launch-day/1381495'
#  
    # dfc = get_replies(driver,url)
    dfc = get_class_page(driver=driver,url=url)
    # print(dfc)
    # dfc.to_csv('output',index=False)
    dfc.to_csv('class_page',index=False)
    driver.quit()

# for next page
# <div role="navigation" itemscope itemtype="http://schema.org/SiteNavigationElement" class="topic-body crawler-post">

# body > div.optanon-alert-box-wrapper.hide-cookie-setting-button > div.optanon-alert-box-bg > div.optanon-alert-box-button-container > div.optanon-alert-box-button.optanon-button-allow > div > button

# <button class="optanon-allow-all accept-cookies-button" title="Accept cookies" aria-label="Accept cookies" onclick="Optanon.TriggerGoogleAnalyticsEvent('OneTrust Cookie Consent', 'Banner Accept Cookies');" tabindex="4">Accept cookies</button>