from selenium import webdriver
from selenium_crawler import main as crawler
import json

"""
Default selenium webdriver setting

variables:
headless_flag   -- selenium chrome browser headless or not
options         -- selenium chrome browser options
"""

headless_flag = True

if headless_flag:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', options=options)
else:
    driver = webdriver.Chrome('chromedriver')

# Wait until driver load resources
driver.implicitly_wait(3)

"""
Main crawling task

file:
selenium_crawler.py

module:
main(location, link, filename, driver)    -- main crawler

main arguments:
location    -- korean location name
link        -- browser menu id
filename    -- path result stored
driver      -- selenium driver
"""

with open('C:/Users/lixxc/PycharmProjects/pythonProject2/location_data.json') as loca_data:
    ld = json.load(loca_data)

for d in ld:
    crawler(d['loca'], d['link'], d['filename'], driver)