import datetime as dt
import copy
import time
import datetime as dt
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.common.by import By


# date setting
tz_asia_seoul = ZoneInfo("Asia/Seoul")
date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')


# crawling setting
# options = webdriver.ChromeOptions()
# options.add_argument("headless") # Make browser invisible
safari = webdriver.Safari()


# load setting
f = open(f'./data/sl_{date}_data.text', 'w')

page = 1
page_previous = None

start = time.time()
while True:
    url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=249&sid1=102&date={date}&page={page}"
    safari.get(url)

    # loop exit condition
    page_num = safari.find_element(By.CLASS_NAME, "paging")
    page_num = page_num.find_element(By.TAG_NAME, "strong").text
    if page_num == page_previous:
       safari.close()
       break
    page_previous = copy.deepcopy(page_num)

    # data crwaling
    elements = safari.find_elements(By.CSS_SELECTOR, "dt:nth-child(2)")
    for element in elements:
        f.write(element.text.strip() + "\n")
    page += 1
end = time.time()

print("done!" + f"{end - start:.5f} sec")
f.close()


