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
            if 'Item' not in response:
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
            else:
                response = table.delete_item(
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
            logging.info('Item (photo_id = ' + photo_id + ') is sucessfully deleted')
            response = {
                'statusCode': 204,
                'body': '',
                'headers': {
                    'Content-Type': 'applicatioin/json',
                }
            }
            logger.info("STEP 5")
            return response
    except Exception as e:
        logger.error('type: %s', type(e))
        logger.error(e)
