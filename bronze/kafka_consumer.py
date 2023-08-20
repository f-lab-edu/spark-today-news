from kafka import KafkaConsumer

import boto3
import Authentication
import ObjectS3
import pandas as pd

import time
import datetime as dt
from zoneinfo import ZoneInfo
from json import loads

# brokers = ['0.0.0.0:9092']
broker = '127.0.0.1:9092'
topic = 'today-news'

tz_asia_seoul = ZoneInfo("Asia/Seoul")
date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')


# set kafka consumer
consumer = KafkaConsumer(
    topic, # 읽어올 토픽 이름
    enable_auto_commit=True, # 완료되었을 때 문자 전송
    # auto_offset_reset="earliest", # 어디서부터 값을 읽어올지 (earlest 가장 처음 latest는 가장 최근)
    # group_id='my-group', # 그룹핑하여 토픽 지정할 수 있다 (같은 컨슈머로 작업)
    bootstrap_servers=broker, # 브로커 주소: 포트번호
    api_version = (0,11,5),
    value_deserializer=lambda v: loads(v.decode('utf-8')), # 역직렬화 ( 받을 떄 )
    # consumer_timeout_ms=1000 # 1000초가 지나면 없는 것으로 취급한다.
)


obj = ObjectS3.ObjectS3()
bucket, object_id = "spnews", f"news{date}"
f = open(f"{object_id}.txt", 'w')
df = pd.DataFrame(columns=['id', 'head','genre','press', 'article_date', 'article_time', 'time', 'article_html'])
for news in consumer:
    df.append(news.value()) # 뉴스 데이터 데이터 프레임에 넣기
    df.to_parquet(f'./data/{object_id}.parquet', compression='gzip') # 현재 위치 파켓 파일 저장
    obj.add_file(bucket, f"{object_id}.parquet", f"./{object_id}.parquet") # 버켓, 저장할 파일 위치,불러올 파일 위치
consumer.close()