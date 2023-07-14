import datetime as dt
import copy
import time

import datetime as dt
from json import dumps
from zoneinfo import ZoneInfo

# Crawling
import requests as req
from bs4 import BeautifulSoup as bs

# Kafka
from kafka import KafkaProducer

brokers = ["localhost:9091","localhost:9092","localhost:9093"]
# set kafka producer
producer = KafkaProducer(
    acks=0,
    compression_type='gzip',
    booststrap_servers=brokers, # 브로커 주소: 포트번호
    value_serializer=lambda v: dumps(v).encode('utf-8'),
)

# date setting
tz_asia_seoul = ZoneInfo("Asia/Seoul")
date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')
page = 1

# crawling setting
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}


# out-string
rm_string = '''
.,"“”‘’[]\|?!
'''
tab_string = '·…'


while True:
    start = time.time()

    rep = req.get(f"https://news.naver.com/main/list.naver?mode=LS2D&mid=sec&sid2=249&sid1=102&date={date}&page={page}" ,headers=header)

    if rep.status_code == 200:
        soup = bs(rep.text, "html.parser")

        headlines = soup.select("dt:nth-child(2)")
        date = soup.select("span.date.is_new")

        for i in range(3):
            try: 
                headline = headline[i].get_text(strip=True)
                date = date[i].get_text()
            except:
                continue

            if '시간전' in date or '일전' in date or '2022' in date:
                continue
            
            # 2분전 데이터를 가져옵니다.
            if int(date.split('분전')[0]) < 2:

                for rm in rm_string:
                    headline = headline.replace(rm, '')
                for tab in tab_string:
                    headline = headline.replace(tab, ' ')
            
            # 토픽(news)와 메세지 보내기
            producer.send('news', {
                'head' : headline
            })

            producer.flush() # 데이터 비우기

    print("done!" + f"{time.time() - start:.5f} sec")


