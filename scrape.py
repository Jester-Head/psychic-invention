from csv import writer
from time import sleep
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import requests


URL = "https://us.forums.blizzard.com/en/wow/t/missed-opportunity-for-df/1367233"


if __name__=="__main__":
    
    page = requests.get(URL)
    sleep(5)
    soup = BeautifulSoup(page.content,"lxml")
    # with open('WowClass',"wb")as w:
    #     w.write(soup)

    print(soup.find('p').prettify(encoding='utf-8'))





