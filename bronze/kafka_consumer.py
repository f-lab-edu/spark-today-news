from kafka import KafkaConsumer

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import boto3
from s3 import Authentication
from s3 import ObjectS3
import pandas as pd

import time
import datetime as dt
from zoneinfo import ZoneInfo
from json import loads
import sys, os

# brokers = ['0.0.0.0:9092']
broker = '127.0.0.1:9092'
topic = 'today-news'

tz_asia_seoul = ZoneInfo("Asia/Seoul")
current_date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')
current_time = dt.datetime.now(tz_asia_seoul).strftime('%H')


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


# Configure S3 Object
obj = ObjectS3.ObjectS3()

# bucket-name, object-id
bucket, object_id = "spnews", f"news{current_date}"
object_id2 = f"{object_id}{current_time}"
f = open(f"data/bronze/{object_id2}.txt", 'w')

# Test 용도
i = 0
for news in consumer:
    i += 1
    data = f"{news.value['id']}| {news.value['head']}| {news.value['genre']}| {news.value['press']}| {news.value['article_date']}| {news.value['article_time']}| {news.value['times']}| {news.value['url']}\n"
    f.write(data)
    print(i)
    if i == 100: # 데이터 갯수
        f.close()
        obj.add_file(bucket, f"{object_id}/{object_id2}.txt", f"data/bronze/{object_id2}.txt") # 버켓, 저장할 파일 위치,불러올 파일 위치
        break


# ## 실제 사용
# for news in consumer:

#     # 시간이 변경된 경우
#     if news.value['article_time'][:2] != current_time:
#         f.close() # 파일쓰기 종료
#         obj.add_file(bucket, f"{object_id}/{object_id2}.txt", f"data/{object_id2}.txt") # s3에 이전 날짜 데이터 저장하기

#         # 만약 날짜가 변경된 것이라면
#         if news.value['article_date'] != current_date:
#             current_date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d') # 날짜 갱신
#             object_id = f"news{current_date}" # 날짜 객체 명 갱신
#             obj.create_folder(bucket, object_id) # 새로운 날짜 폴더 생성

#         # 시간 갱신 후 시간 객체 갱신(파일명)
#         current_time = dt.datetime.now(tz_asia_seoul).strftime('%H%M')
#         object_id2 = f"{object_id}{current_time}"
#         f = open(f"data/{object_id2}.txt", 'w') # 파일 열기
    
#     data = f"{news.value['id']}| {news.value['head']}| {news.value['genre']}| {news.value['press']}| {news.value['article_date']}| {news.value['article_time']}| {news.value['times']}| {news.value['url']}\n"
#     f.write(data)

consumer.close()