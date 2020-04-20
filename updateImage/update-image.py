import boto3
import uuid
import json
import logging
import os
import datetime
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Lambda関数にせっとする変数は環境変数を利用する
# DB接続処理は比較的重い処理
# lambda_handler内に記述するとコールドスタート/ウォームスタート
# に限らず処理の重いDB接続処理が毎回行われてしまう
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

"""
バリデーション関数
"""
def validate(request_body):
    return request_body.keys() >= { "photo_id" , "timestamp" , "status"}

def lambda_handler(event, context):
    logger.info("STEP 1")
    body = json.loads(event['body'])
    if not validate(body):
        error_response = {
            'statusCode': '400',
            'body': 'Validation error',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    logger.info("STEP 2")
    photo_id = body['photo_id']
    timestamp = body['timestamp']
    status = body['status']

    logger.info("STEP 3")
    try:
        try:
            table.update_item(
                Key={
                    'photo_id': photo_id
                },
                AttributeUpdates={
                    'status': {
                        'Value': status,
                        'Action': 'PUT'
                    }
                }
            )
            logger.info("STEP 4")
            response = table.get_item(
                Key={
                    'photo_id': photo_id
                }
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
            response = {
                'statusCode': 400,
                'body': e.response['Error']['Message'],
                'headers': {
                    'Content-Type': 'applicatioin/json',
                    'Access-Control-Allow-Origin': '*'
                },
            }
            logger.info("STEP 5")
            return response
        else:
            items = json.dumps(response['Item'], cls=DecimalEncoder)
            response = {
                'statusCode': 200,
                'body': items,
                'headers': {
                    'Content-Type': 'applicatioin/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            logger.info("STEP 5")
            return response
    except Exception as e:
        logger.error('type: %s', type(e))
        logger.error(e)
