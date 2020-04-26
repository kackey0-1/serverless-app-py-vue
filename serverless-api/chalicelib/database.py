import os
import uuid
import boto3
from boto3.dynamodb.conditions import Key
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDBへの接続を取得する
def _get_database():
    endpoint = os.environ.get('DB_ENDPOINT')
    region_name = os.environ.get('DB_REGION')
    if endpoint:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
        return boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
        return boto3.resource('dynamodb', region_name=region_name)

# すべてのレコードを取得する
def get_all_images(table_name):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning
    response = table.scan()
    return response['Items']

# 指定されたIDのレコードを取得する
def get_image(image_id):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning
    response = table.query(
        KeyConditionExpression=Key('id').eq(image_id)
    )
    items = response['Items']
    return items[0] if items else None

# レコードを登録する
def create_image(image):
    now = datetime.datetime.now()
    # 登録内容を作成する
    item = {
        'id': uuid.uuid4().hex,
        'title': image['title'],
        'size': image['size'],
        'status': image['status'],
        'timestamp': now,
        'type': image['type'],
    }

    # DynamoDBにデータを登録する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#creating-a-new-item
    table.put_item(Item=item)
    return item

# 指定されたIDのレコードを更新する
def update_image(image_id, changes):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # クエリを構築する
    update_expression = []
    expression_attribute_values = {}
    for key in ['title', 'memo', 'priority', 'completed']:
        if key in changes:
            update_expression.append(f"{key} = :{key[0:1]}")
            expression_attribute_values[f":{key[0:1]}"] = changes[key]

    # DynamoDBのデータを更新する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#updating-item
    result = table.update_item(
        Key={
            'id': image_id,
        },
        UpdateExpression='set ' + ','.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']

# 指定されたIDのレコードを削除する
def delete_image(image_id):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # DynamoDBのデータを削除する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#deleting-item
    result = table.delete_item(
        Key={
            'id': image_id,
        },
        ReturnValues='ALL_OLD'
    )
    return result['Attributes']

