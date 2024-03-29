from dotenv import load_dotenv
import boto3
import uuid
import os


class S3ImgUploader:
    def __init__(self, file):
        self.file = file

    def upload(self, folder):
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        url = folder+'/'+uuid.uuid1().hex
        s3_client.upload_fileobj(self.file, os.environ.get("AWS_STORAGE_BUCKET_NAME"), url, ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url
    
    def delete(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

        try:
            s3_client.delete_object(
                Bucket=os.environ.get("AWS_STORAGE_BUCKET_NAME"),
                Key=str(self.file)  
            )
            return True  
        except Exception as e:
            print("S3 이미지 삭제 실패:", str(e))
            return False