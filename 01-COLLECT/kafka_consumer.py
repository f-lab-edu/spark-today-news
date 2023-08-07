from kafka import KafkaConsumer
from json import loads
# brokers = ['0.0.0.0:9092']
brokers = ['175.45.203.105:66535']

# set kafka consumer
consumer = KafkaConsumer(
    'new-topic', # 읽어올 토픽 이름
    enable_auto_commit=True, # 완료되었을 때 문자 전송
    # auto_offset_reset="earliest", # 어디서부터 값을 읽어올지 (earlest 가장 처음 latest는 가장 최근)
    # group_id='my-group', # 그룹핑하여 토픽 지정할 수 있다 (같은 컨슈머로 작업)
    bootstrap_servers=brokers, # 브로커 주소: 포트번호
    api_version = (0,11,5),
    value_deserializer=lambda v: loads(v.decode('utf-8')), # 역직렬화 ( 받을 떄 )
    # consumer_timeout_ms=1000 # 1000초가 지나면 없는 것으로 취급한다.
)


for news in consumer:
    print(f"{news.value['head', 'date', 'genre']}")

consumer.close()