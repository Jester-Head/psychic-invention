# # __author__ = "Soumil Shah"
# # __email__ = "shahsoumil519@gmail.com"
# try:

#     import os
#     import sys
#     import time

#     from bs4 import BeautifulSoup
#     from fake_useragent import UserAgent
#     from fp.fp import FreeProxy
#     from selenium import webdriver
#     from selenium.common.exceptions import TimeoutException
#     from selenium.webdriver import Chrome
#     from selenium.webdriver.chrome.options import Options
#     from selenium.webdriver.common.action_chains import ActionChains
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.common.keys import Keys
#     from selenium.webdriver.support import expected_conditions as EC
#     from selenium.webdriver.support.ui import WebDriverWait
#     from selenium.webdriver.chrome.service import Service
#     import undetected_chromedriver.v2 as uc

#     print('all module are loaded ')

# except Exception as e:

#     print("Error ->>>: {} ".format(e))


# class Spoofer(object):

#     def __init__(self, country_id=['US'], rand=True, anonym=True):
#         self.country_id = country_id
#         self.rand = rand
#         self.anonym = anonym
#         self.userAgent, self.ip = self.get()

#     def get(self):
#         ua = UserAgent()
#         proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
#         ip = proxy.split("://")[1]
#         return ua.random, ip


# class DriverOptions(object):

#     def __init__(self):

#         self.options = Options()
#         self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--start-maximized')
        # self.options.add_argument('--start-fullscreen')
#         self.options.add_argument('--single-process')
#         self.options.add_argument('--disable-dev-shm-usage')
#         # self.options.add_argument("--incognito")
#         self.options.add_argument('--disable-blink-features=AutomationControlled')
#         self.options.add_experimental_option('useAutomationExtension', False)
#         self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         self.options.add_argument("disable-infobars")

#         self.helperSpoofer = Spoofer()

#         self.options.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
#         self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)


# class WebDriver(DriverOptions):

#     def __init__(self, path=''):
#         DriverOptions.__init__(self)
#         self.driver_instance = self.get_driver()

#     def get_driver(self):

#         print("""
#         IP:{}
#         UserAgent: {}
#         """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))

#         PROXY = self.helperSpoofer.ip
#         webdriver.DesiredCapabilities.CHROME['proxy'] = {
#             "httpProxy":PROXY,
#             "ftpProxy":PROXY,
#             "sslProxy":PROXY,
#             "noProxy":None,
#             "proxyType":"MANUAL",
#             "autodetect":False
#         }
#         webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

#         # path = os.path.join(os.getcwd(), '../windowsDriver/chromedriver.exe')

#         # driver = webdriver.Chrome(executable_path=path, options=self.options)
#         service = Service('C:\chromedriver_win32\chromedriver')
#         driver = webdriver.Chrome(service=service)
#         driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#         driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#             "source":
#                 "const newProto = navigator.__proto__;"
#                 "delete newProto.webdriver;"
#                 "navigator.__proto__ = newProto;"
#         })

#         return driver


# def main():

#     driver= WebDriver()
#     driverinstance = driver.driver_instance
#     driverinstance.get("https://nowsecure.nl")
#     time.sleep(5)
#     print("done")
import time
import undetected_chromedriver.v2 as uc

if __name__ == "__main__":
    #     main()
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
    options.add_argument('--start-fullscreen')


    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = uc.Chrome(options=options)
    
    
    with driver:
        driver.get('https://nowsecure.nl')  # known url using cloudflare's "under attack mode"
        # driver.sleep(30)
        # driver.get('https://amiunique.org/fp')
        time.sleep(60)
        driver.quit()
        
        

