import datetime
import boto3
import os

def get_timestamp():
    now = datetime.datetime.utcnow()
    return int(now.timestamp())

"""
署名付きURLの発行
"""
def get_presigned_url(bucket_name, key, type):
    region_name = os.environ.get("REGION_NAME")
    s3 = boto3.client('s3', region_name=region_name)
    url = s3.generate_presigned_url(
        ClientMethod = 'put_object',
        Params = {
            'Bucket': bucket_name,
            'Key': key,
            'ContentType': type
            },
        ExpiresIn = 3600,
        HttpMethod = 'PUT',
        )
    return url