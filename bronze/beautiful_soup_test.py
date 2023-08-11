import datetime as dt
import copy
import time
import requests as req
import datetime as dt
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup as bs

# date setting
tz_asia_seoul = ZoneInfo("Asia/Seoul")
date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')

# crawling setting
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}

# load setting
f = open(f'./data/bf_{date}_data.text', 'w')

page = 1
page_previous = None

start = time.time()
while True:
    url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=sec&sid2=249&sid1=102&date={date}&page={page}"
    rep = req.get(url, headers=header)
    if req.status_codes == 200:
        soup = bs(rep.text, "html.parser")

        # loop exit condition
        page_num = soup.select_one('#main_content > div.paging > strong').text
        if page_num == page_previous:
            break
        page_previous = copy.deepcopy(page_num)
        
        # data crwaling
        headlines = soup.select("dt:nth-child(2)")
        date = soup.select("span.date.is_new")
        for headline in headlines:
            f.write(headline.get_text(strip=True) + "\n")
        page += 1
end = time.time()

print("done!" + f"{end - start:.5f} sec")
f.close()


