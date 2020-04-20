import boto3
import uuid
import json
import logging
import os
import datetime
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

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

def lambda_handler(event, context):
    logger.info("STEP 1")
    try:
        photo_id = event['pathParameters']['id']
        try:
            response = table.get_item(
                Key={
                    'photo_id': photo_id
                }
            )
            logger.info("STEP 2")
            if 'Item' in response:
                logger.info("Specified key is not found.")
                response = {
                    'statusCode': 404,
                    'body': "Not Found",
                    'headers': {
                        'Content-Type': 'applicatioin/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                }
                return response
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
            return response
        else:
            logger.info("STEP 3")
            items = json.dumps(response['Items'], cls=DecimalEncoder)
            response = {
                'statusCode': 200,
                'body': items,
                'headers': {
                    'Content-Type': 'applicatioin/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            return response
    except Exception as e:
        logger.error('type: %s', type(e))
        logger.error(e)
