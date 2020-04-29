from chalice import BadRequestError, Chalice, NotFoundError
from chalicelib import database, utils
from chalice import CognitoUserPoolAuthorizer
import os

authorizer = CognitoUserPoolAuthorizer(
    'ChaliceUserPool', provider_arns=[os.environ['USER_POOL_ARN']]
)

app = Chalice(app_name='videos-api')
# TABLE_NAME = 'videos'
# すべてのvideoを取得する
@app.route('/videos', methods=['GET'], cors=True, authorizer=authorizer)
def get_all_videos():
    return database.get_all_videos()

# 指定されたIDのvideoを取得する
@app.route('/videos/{video_id}', methods=['GET'], cors=True, authorizer=authorizer)
def get_video(video_id):
    app.log.debug("success")
    video = database.get_video(video_id)
    if video:
        return video
    else:
        # 404を返す
        raise NotFoundError('video not found.')

# videoを登録する
@app.route('/videos', methods=['POST'], cors=True, authorizer=authorizer)
def create_video():
    # リクエストメッセージボディを取得する
    video = app.current_request.json_body
    app.log.debug(app.current_request.json_body)
    # 必須項目をチェックする
    for key in ['title', 'type', 'size']:
        if key not in video:
            raise BadRequestError(f"{key} is required.")
    # データを登録する
    return database.create_video(video, utils.get_timestamp())

# 指定されたIDのvideoを更新する
@app.route('/videos/{video_id}', methods=['PUT'], cors=True, authorizer=authorizer)
def update_video(video_id):
    changes = app.current_request.json_body

    # データを更新する
    return database.update_video(video_id, changes)

# 指定されたIDのvideoを削除する
@app.route('/videos/{video_id}', methods=['DELETE'], cors=True, authorizer=authorizer)
def delete_video(video_id):
    # データを削除する
    return database.delete_video(video_id)
