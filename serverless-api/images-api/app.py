from chalice import BadRequestError, Chalice, NotFoundError
from chalicelib import database, utils
from chalice import CognitoUserPoolAuthorizer
import os
import logging

authorizer = CognitoUserPoolAuthorizer(
    'ChaliceUserPool', provider_arns=[os.environ['USER_POOL_ARN']]
)

app = Chalice(app_name='images-api')
app.log.setLevel(logging.INFO)

# TABLE_NAME = 'Images'
# すべてのImageを取得する
@app.route('/images', methods=['GET'], cors=True, authorizer=authorizer)
def get_all_images():
    return database.get_all_images()

# 指定されたIDのImageを取得する
@app.route('/images/{image_id}', methods=['GET'], cors=True, authorizer=authorizer)
def get_image(image_id):
    app.log.debug("success")
    image = database.get_image(image_id)
    if image:
        return image
    else:
        # 404を返す
        raise NotFoundError('image not found.')

# imageを登録する
@app.route('/images', methods=['POST'], cors=True, authorizer=authorizer)
def create_image():
    # リクエストメッセージボディを取得する
    image = app.current_request.json_body
    app.log.info(app.current_request.json_body)
    # 必須項目をチェックする
    for key in ['title', 'type', 'size']:
        if key not in image:
            raise BadRequestError(f"{key} is required.")
    # データを登録する
    app.log.debug(utils.get_timestamp())
    image = database.create_image(image, utils.get_timestamp())
    url = utils.get_presigned_url(os.getenv('IMAGES_BUCKET_NAME'), image['image_id'] + "." + image['type'].split("/")[1], image['type'])
    image["signed_url"] = url
    return image

# 指定されたIDのimageを更新する
@app.route('/images', methods=['PUT'], cors=True, authorizer=authorizer)
def update_image():
    changes = app.current_request.json_body
    # データを更新する
    return database.update_image(changes['image_id'], changes)

# 指定されたIDのimageを削除する
@app.route('/images/{image_id}', methods=['DELETE'], cors=True, authorizer=authorizer)
def delete_image(image_id):
    # データを削除する
    return database.delete_image(image_id)
