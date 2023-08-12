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
# brokers = ['0.0.0.0:9092']
broker = '175.45.203.105:9093'
# set kafka producer
producer = KafkaProducer(
    acks=0, # 메시지 받는 사람이 잘  받았는지 체크하는 옵션 (0은 확인 없이그냥 보내기)
    compression_type='gzip', # 메시지 전달할 때  압축
    bootstrap_servers=broker, # 브로커 주소: 포트번호
    value_serializer=lambda v: dumps(v).encode('utf-8'), # 데이터 전송을 위해 byte 단위로 바꿔주는 작업
    api_version = (0,11,5)
)

# date setting
tz_asia_seoul = ZoneInfo("Asia/Seoul")
date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')

# crawling setting
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"}
genres = {'100':'정치', '101':'경제', '102':'사회', '103':'문화'}


while True:
    for genre in genres.keys():
        start = time.time()
        rep = req.get(f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={genre}" ,headers=header)

        if rep.status_code == 200:
            time.sleep(2)
            html = rep.text
            soup = bs(html, "html.parser")
            headlines = soup.select("dt:nth-child(2) > a")
            dates = soup.select("span.date.is_new")
            presses = soup.select("span.writing")
            for i in range(3):
                try: 
                    url = headlines[i]['href']
                    id = url.split("?")[0].replace("https://n.news.naver.com/mnews/article/", "").replace("/", "-")
                    headline = headlines[i].get_text(strip=True)
                    press = presses[i].get_text(strip=True)
                    subhtml = req.get(url).text
                    date = dates[i].get_text()
                except:
                    continue

                if '시간전' in date or '일전' in date or '2022' in date:
                    continue
                
                # 2분전 데이터를 가져옵니다.
                if int(date.split('분전')[0]) < 2:
                    times = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d %H:%M:%S')
                    gen = genres[genre]
                    
                    print(id, headline, times, gen, press, subhtml)

                    # 토픽(news)와 메세지 보내기
                    producer.send('new-topic', {
                        'id' : id,
                        'head' : headline,
                        'date' : times,
                        'genre' : gen,
                        'press' : press,
                        'html' : subhtml
                    })
                    producer.flush() # 데이터 비우기

# print("done!" + f"{time.time() - start:.5f} sec")


