import boto3
import uuid
import json
import logging
import os
import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lambda関数にせっとする変数は環境変数を利用する
# DB接続処理は比較的重い処理
# lambda_handler内に記述するとコールドスタート/ウォームスタート
# に限らず処理の重いDB接続処理が毎回行われてしまう
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

"""
画像保存時のキーとなるIDを発行(UUIDメソッドより発行)
"""
def generate_id():
    return str(uuid.uuid4())

"""
TIMESTAMPの取得
"""
def get_timestamp():
    now = datetime.datetime.utcnow()
    return int(now.timestamp())

"""
署名付きURLの発行
"""
def get_presigned_url(bucket_name, key, type):
    s3 = boto3.client('s3', region_name='ap-northeast-1')
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

def lambda_handler(event, context):
    logger.info("STEP 1")
    body = json.loads(event['body'])
    logger.info("STEP 2")
    ext = body['type'].split('/')[1]
    logger.info("STEP 3")
    photo_id = generate_id()
    logger.info("STEP 4")
    url = get_presigned_url(os.getenv('BUCKET_NAME'), photo_id + "." + ext, body['type'])
    logger.info("STEP 5")
    item = {
        'photo_id': photo_id,
        'timestamp': get_timestamp(),
        'status': 'Waiting',
        'type': body['type'],
        'size': body['size']
    }
    logger.info("STEP 6")
    try:
        table.put_item(
            Item = item
        )
        logger.info("STEP 7")
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
        response = {
            'statusCode': 400,
            'body': e.response['Error']['Message'],
            'headers': {
                'Content-Type': 'applicatioin/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
        logger.info("STEP 8")
        return response
    else:
        item['signed_url'] = url
        response = {
            'statusCode': 200,
            'body': json.dumps(item),
            'headers': {
                'Content-Type': 'applicatioin/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
        logger.info("STEP 8")
        return response
