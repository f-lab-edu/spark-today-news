from kafka import KafkaConsumer
from json import loads

brokers = ["localhost:9091","localhost:9092","localhost:9093"]

# set kafka consumer
consumer = KafkaConsumer(
    compression_type='gzip',
    booststrap_servers=brokers, # 브로커 주소: 포트번호
    value_deserializer=lambda v: loads(v.decode('utf-8')),
)


for news in consumer:
    print(f"{news.value['head']}")

consumer.close()