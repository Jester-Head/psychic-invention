from csv import writer
from encodings.utf_8 import encode
from itertools import tee
from re import S
from time import sleep
from types import new_class
from bs4 import BeautifulSoup,SoupStrainer
from bs4 import NavigableString
# from bs4 import UnicodeDammit
import requests


URL = "https://us.forums.blizzard.com/en/wow/t/missed-opportunity-for-df/1367233"

def test_bs4():
    page = requests.get(URL)
    sleep(5)
    soup = BeautifulSoup(page.content,"lxml")
    
    with open('WowClass',"wb")as w:
        w.write(soup.prettify(encoding="utf-8"))

    # print(soup.find_all('p')) 
    # new_str = soup.find_all('p')
    # div class="post" itemprop="articleBody"

    # print(type(new_str))
    # print(soup.prettify(encoding='utf-8'))
    # for tag in soup.find_all(True):
    #     print(tag.name)
    only_p_tags = SoupStrainer("p")
    with open('WowClass',encoding="utf8")as f:
        text = BeautifulSoup(f,'lxml',parse_only=only_p_tags)
    # print(text.find_all('p'))
    print(list(text.stripped_strings)[1])

def get_top_posts():
    page = requests.get('https://us.forums.blizzard.com/en/wow/c/classes/174/l/top?period=quarterly')
    sleep(5)
    only_a_tags = SoupStrainer("a")
    soup = BeautifulSoup(page.content,"lxml",from_encoding='utf-8',parse_only=only_a_tags)
    # text = soup.find_all(['td','a'])
    # text = soup.find_all('a')
    
    # table class='topic-list'
    print(soup['class'])
    # print(soup.prettify(encoding="utf-8"))
    # print(text)


if __name__=="__main__":
    
    get_top_posts()

    

   
   



