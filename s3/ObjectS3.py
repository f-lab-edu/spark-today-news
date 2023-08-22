import boto3 # pip3 install boto3==1.6.19
from . import Authentication
import json

class ObjectS3:
    def __init__(self):
        self.service_name = 's3'
        self.endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.region_name = 'kr-standard'
        self.access_key = Authentication.get_access_key()
        self.secret_key = Authentication.get_secret_key()
        self.s3 = boto3.client(self.service_name, endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

    # 버킷 추가 (중복검사 수행 필요)
    def add_bucket(self,bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            return print({"target":bucket_name, "result":"success"})
        except:
            return print({"target":bucket_name, "result":"fail"})
        
    # 버킷 제거
    def del_bucket(self,bucket_name):
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            return {"target":bucket_name, "result":"success"}
        except:
            return {"target":bucket_name, "result":"fail"}

    # 버킷 목록
    def get_bucket_list(self):
        response = self.s3.list_buckets()
        for bucket in response.get('Buckets', []):
            print(bucket.get('Name'))
        return {"result":"success"}

    # 폴더 생성
    def create_folder(self, bucket_name, object_name):
        # object 이름 마지막 '/' 추가
        if (object_name.strip()[-1] != '/'):
            object_name = object_name + '/'
        
        # object 이름 맨 앞 '/' 제거
        if (object_name[0] == '/'):
            object_name = object_name[1:]

        overlap_chk = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=object_name, MaxKeys=1)
        if ('Contents' in overlap_chk):
            return {"target":object_name, "result":"fail"}
        else:
            self.s3.put_object(Bucket=bucket_name, Key=object_name)
            return {"target":object_name, "result":"success"}

    # 폴더 제거
    def del_folder(self,bucket_name,object_name):
        # object 이름 마지막 '/' 추가
        if (object_name.strip()[-1] != '/'):
            object_name = object_name + '/'
        
        # object 이름 맨 앞 '/' 제거
        if (object_name[0] == '/'):
            object_name = object_name[1:]

        overlap_chk = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=object_name, MaxKeys=1)
        if ('Contents' in overlap_chk):
            return {"target":object_name, "result":"fail"}
        else:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            return {"target":object_name, "result":"success"}


    # 파일 업로드
    def add_file(self,bucket_name,object_name,local_file_path):
        try:
            self.s3.upload_file(local_file_path, bucket_name, object_name)
            return print({"target":object_name,"result":"success"})
        except:
            return print({"target":object_name,"result":"fail"})

    # 파일 다운로드
    def get_file(self,bucket_name,object_name,local_file_path):
        try:
            self.s3.download_file(bucket_name, object_name, local_file_path)
            return {"target":object_name, "result":"success"}
        except:
            return {"target":object_name,"result":"fail"}

    # 파일 제거
    def del_file(self,bucket_name,object_name):
        file_chk = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=object_name, MaxKeys=1)
        if ('Contents' in file_chk):
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            return {"target":object_name, "result":"success"}
        else:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            return {"target":object_name, "result":"fail"}

    # 파일 목록
    def get_file_list(self, bucket_name, path='', delimiter_mode='n'):
        if (delimiter_mode == 'y'):
            delimiter = '/'
        elif (delimiter_mode == 'n'):
            delimiter = ''

        max_keys = 300
        try:
            response = self.s3.list_objects(Bucket=bucket_name, Prefix=path, Delimiter=delimiter, MaxKeys=max_keys) # prefix(접두사), Delimiter(구분기호)
        except:
            return {"target":bucket_name, "path":path, "result":"fail"}

        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if (status_code == 200):
            data = []
            for i in response.get('Contents'):
                data.append(i['Key'])
            return {"target":bucket_name, "path":path, "data":data, "result":"success"}
        else:
            return {"target":bucket_name, "path":path, "result":"fail"}