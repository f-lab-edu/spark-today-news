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

### RedPanda 설치
```zsh
## Run the setup script to download and install the repo
curl -1sLf 'https://dl.redpanda.com/nzc4ZYQK3WRGd9sy/redpanda/cfg/setup/bash.deb.sh' | sudo -E bash && \
## Use apt to install redpanda
sudo apt install redpanda -y && \
## Start redpanda as a service 
sudo systemctl start redpanda
```
```zsh
# 확인
sudo systemctl status redpanda
```

---

## 참고

```zsh
sudo apt-get purge --auto-remove python3.5
```