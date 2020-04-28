from chalice import BadRequestError, Chalice, NotFoundError
from chalicelib import database, utils

app = Chalice(app_name='severless-api')
# TABLE_NAME = 'Images'
# すべてのImageを取得する
@app.route('/images', methods=['GET'], cors=True)
def get_all_images():
    return database.get_all_images()

# 指定されたIDのImageを取得する
@app.route('/images/{image_id}', methods=['GET'], cors=True)
def get_image(image_id):
    app.log.debug("success")
    image = database.get_image(image_id)
    if image:
        return image
    else:
        # 404を返す
        raise NotFoundError('image not found.')

# imageを登録する
@app.route('/images', methods=['POST'], cors=True)
def create_image():
    # リクエストメッセージボディを取得する
    image = app.current_request.json_body
    app.log.debug(app.current_request.json_body)
    # 必須項目をチェックする
    for key in ['title', 'type', 'size']:
        if key not in image:
            raise BadRequestError(f"{key} is required.")
    # データを登録する
    return database.create_image(image, utils.get_timestamp())

# 指定されたIDのimageを更新する
@app.route('/images/{image_id}', methods=['PUT'], cors=True)
def update_image(image_id):
    changes = app.current_request.json_body

    # データを更新する
    return database.update_image(image_id, changes)

# 指定されたIDのimageを削除する
@app.route('/images/{image_id}', methods=['DELETE'], cors=True)
def delete_image(image_id):
    # データを削除する
    return database.delete_image(image_id)
