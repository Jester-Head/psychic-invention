
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import no_detect




def get_class_page(driver,url):
    driver.get(url)
    time.sleep(5)
    
    author = driver.find_elements(By.CSS_SELECTOR,'td.creator')
    author = [c.text for c in author]
    
    topic = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix')
    topic = [t.text for t in topic]

    replies = driver.find_elements(By.CSS_SELECTOR,'td.num.posts-map.posts.topic-list-data > button > span')
    replies = [r.text for r in replies]

    views = driver.find_elements(By.CSS_SELECTOR,'td.num.views > span')
    views = [v.text for v in views]

    link = driver.find_elements(By.CSS_SELECTOR,'td.main-link.clearfix > span > a')
    link = [l.get_attribute('href') for l in link]
    driver.quit()

    df = pd.DataFrame(list(zip(topic,author,views,replies)),columns=['topic','author','views','replies'])
    return df

def get_replies(driver,url):
    time.sleep(5)
    driver.get(url)
    # comments = driver.find_elements(By.CSS_SELECTOR,'p')
    # comments = driver.find_elements(By.CSS_SELECTOR,'div > div.topic-body.clearfix > div.regular.contents > div')
    comments = driver.find_elements(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "post-stream", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "highlighted", " " ))]')
    # comments = driver.find_elements(By.XPATH,'.//*[@id="post_1"]/div/div[2]/div[2]/div[1]')
    comments = [com.text for com in comments]
    # comments = comments[3:]
    time.sleep(5)
    author = driver.find_elements(By.XPATH,'.//*[contains(concat( " ", @class, " " ), concat( " ", "character-name", " " ))]')
    author = [a.text for a in author]
    
    df = pd.DataFrame(list(zip(comments,author)),columns=['comments','author'])
    return df
    


if __name__== "__main__":
    
    # service = Service('C:\chromedriver_win32\chromedriver')
    # driver = webdriver.Chrome(service=service)
    # url = 'https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175'
    url = 'https://us.forums.blizzard.com/en/wow/t/please-fix-momentum-before-launch-day/1381495'
 
    
    driver= no_detect.WebDriver()
    driver_instance = driver.driver_instance
    # df = get_class_page(url=url,driver=driver_instance)
    dfc = get_replies(driver_instance,url)
    # dfc = pd.DataFrame(data = comments,columns=['comments'])
    print(dfc)
    driver_instance.quit()
# for next page
# <div role="navigation" itemscope itemtype="http://schema.org/SiteNavigationElement" class="topic-body crawler-post">