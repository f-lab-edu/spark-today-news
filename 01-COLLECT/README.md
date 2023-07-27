# Settings Cloud Platform

이번 프로젝트에서는 NaverCloud를 이용해 서버를 구축하고 Redpanda를 통해 실시간 네이버 뉴스 데이터를 Consumer로 보내 S3에 수집하는 작업을 진행하려고 합니다.

## Naver Cloud Server 구축
### VPC, Subnet, Server 구축
- VPC, Subnet, Server 구축

### 서버내 패키지 설치
- 서버내 기본 apt 설치
```zsh
sudo apt update && \
sudo apt install build-essential -y
sudo apt install curl
```

- 서버내 파이썬 버전 설치 : *3.9.14*
```zsh
# 파이썬 버전 설치
wget https://www.python.org/ftp/python/3.9.14/Python-3.9.14.tgz
# 압축 해제
tar -xf Python-3.9.14.tgz

# 파이썬 3.9.14 설정 스크립트
cd Python 3.9.14
./configure --enable-optimizations

# 빌드
make -j 12

# 파이썬 바이너리 설치
sudo make altinstall

# 버전 확인
python3.9.14 -V
sudo apt install python3 -y

# 이미 존재하는 다른버전의 python을 현재 설치한 파이썬 버전으로 python 명령어 입력하여 메인으로 사용하고 싶을 때
update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1


# 패키지 관리자 설치
sudo apt install python3-pip
```

### Kafka 설치
```zsh
wget https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz \
&& tar xzf kafka_2.13-3.5.0.tgz
```

```zsh
echo 'export KAFKA_HOME=/root/kafka_2.13-3.5.0' >> ~/.bashrc \
&& source ~/.bashrc
```

### 카프카 보안 그룹내 통신 설정

|IP|Port|비고|
|---|---|---|
|0.0.0.0/0|2181|Zookeeper|
|0.0.0.0/0|9092|Kafka|
|내 PC IP|22|SSH|


### Broker Server

1. 주키퍼 서버 실행

```
 //opt/kafka_2.12-3.4.1/bin/zookeeper-server-start.sh //opt/kafka_2.12-3.4.1/config/zookeeper.properties
```

2. 다른 터미널로 카프카 서버 실행

```
 //opt/kafka_2.12-3.4.1/bin/kafka-server-start.sh //opt/kafka_2.12-3.4.1/config/server.properties
```

3. 다른 터미널로 토픽 생성

```
//opt/kafka_2.12-3.4.1/bin/kafka-topics.sh --create --topic new-topic --bootstrap-server 175.45.203.105:9092
```

### Producer

부트스트랩 서버를 `Broker`서버로 설정하여 토픽을 전송합니다.

```
opt/kafka_2.13-3.5.0/bin/kafka-console-producer.sh  --topic new-topic --bootstrap-server 175.45.203.105:9092
```


### consumer

```
opt/kafka_2.13-3.5.0//bin/kafka-console-consumer.sh --topic new-topic --from-beginning --bootstrap-server 175.45.203.105:9092
```

---

### 로컬에서 실시간 데이터 전송하기
- local에서 kafka-python을 이용해 데이터를 전송하려고 했으나 전송이 되지 않음.

