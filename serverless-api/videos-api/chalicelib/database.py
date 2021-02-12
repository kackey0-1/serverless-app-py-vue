import os
import uuid
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
def get_all_videos():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning
    response = table.scan()
    return response['Items']

# 指定されたIDのレコードを取得する
def get_video(video_id):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning
    response = table.query(KeyConditionExpression=Key('video_id').eq(video_id))
    items = response['Items']
    return items if items else None

# レコードを登録する
def create_video(video, now):
    # 登録内容を作成する
    item = {
        'video_id': uuid.uuid4().hex,
        'title': video['title'],
        'size': video['size'],
        'status': "Uploaded",
        'timestamp': now,
        'type': video['type'],
    }
    
    # DynamoDBにデータを登録する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#creating-a-new-item
    table.put_item(Item=item)
    return item

# 指定されたIDのレコードを更新する
def update_video(video_id, changes):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # クエリを構築する
    update_expression = []
    expression_attribute_names = {}
    expression_attribute_values = {}
    for key in ['title', 'size', 'type']:
        if key in changes:
            update_expression.append(f"#{key} = :{key}")
            expression_attribute_names[f"#{key}"] = key
            expression_attribute_values[f":{key}"] = changes[key]
    # DynamoDBのデータを更新する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#updating-item
    result = table.update_item(
        Key={
            'video_id': video_id,
        },
        UpdateExpression='set ' + ','.join(update_expression),
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']

# 指定されたIDのレコードを削除する
def delete_video(video_id):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # DynamoDBのデータを削除する
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#deleting-item
    result = table.delete_item(
        Key={
            'video_id': video_id,
        },
        ReturnValues='ALL_OLD'
    )
    return result['Attributes']

