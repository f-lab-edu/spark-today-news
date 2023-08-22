import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from s3 import Authentication
from s3 import ObjectS3
import datetime as dt
from zoneinfo import ZoneInfo

from pyspark.sql import (Row, SparkSession)
from pyspark.sql.functions import col, asc, desc, round as rnd



tz_asia_seoul = ZoneInfo("Asia/Seoul")
current_date = dt.datetime.now(tz_asia_seoul).strftime('%Y%m%d')
current_time = dt.datetime.now(tz_asia_seoul).strftime('%H')

# Configure S3 Object
obj = ObjectS3.ObjectS3()
bucket, object_id = "spnews", f"news{current_date}"
object_id2 = f"{object_id}{current_time}"

# 데이터를 다운 받아 전처리 실행
obj.get_file(bucket, f"{object_id}/{object_id2}.txt", f"data/silver/{object_id2}.txt")


"""
Spark
"""

# SparkContext 객체 생성
spark =SparkSession.builder.appName("spnews_nb")\
      .master("local[*]").config("spark.driver.memory","5g")\
      .config("spark.driver.host","127.0.0.1")\
      .config("spark.driver.bindAddress","127.0.0.1")\
      .getOrCreate()

def parse_line(line:str):
    fields = line.split("| ")
    return Row(
        id=str(fields[0]),
        head=str(fields[1]),
        genre=str(fields[2]),
        press=str(fields[3]),
        article_date=str(fields[4]),
        article_time=str(fields[5]),
        times = str(fields[6]),
        url = str(fields[7]))

# 데이터 가져오기
lines = spark.sparkContext.textFile(f"data/silver/{object_id2}.txt")
income_data = lines.map(parse_line)

# RDD를 데이터 프레임으로 변환하기
schema_income = spark.createDataFrame(data=income_data)
schema_income.createOrReplaceTempView("income")


# 데이터 전처리


df = spark.sql(
    """
    SELECT distinct(id), head, genre, press, article_date, article_time
    from income
    """
)


# 골드 레이어 데이터 저장 coalesce는 파티션의 수를 의미합니다.
df.coalesce(1).write.option("heaer","true").csv(f"data/gold/{object_id2}")