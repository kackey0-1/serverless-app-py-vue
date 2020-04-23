# サーバーレスアプリケーションを作成する

## 手順
1. Webコンテンツ用のS3用意
2. API実装(S3 + DynamoDB + API Gateway + Lambda実装) *プログラムファイル作成まで完了
3. クライアントアプリ(vuejs)実装
4. 認証機能実装(Amazon Cognitoの用意)
5. 画像解析機能実装(Amazon Rekognitionの用意)

<!-- ## Lambdaローカル検証環境 for python
1. `pip install python-lambda-local`
2. `python-lambda-local -l lib/ -f handler -t 15 <test_file>.py <parameter_file>.json` -->

### Webコンテンツ用のS3用意
#### backet作成
`aws s3 mb s3://serverless-app-web-vue --region ap-northeast-1`
#### webホスティングを有効
`aws s3 website s3://serverless-app-web-vue/ --index-document index.html`
#### アクセスポリシー作成
`aws s3api put-bucket-policy --bucket serverless-app-web-vue --policy file://policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::serverless-app-web-vue/*"
    }
  ]
}
```

#### S3へファイルアップロード
`aws s3 sync ~/webapp/ s3://serverless-app-web-vue/`

### API実装(API Gateway + Lambda実装)
#### API Gatewayを利用するメリット
```txt
通常APIサーバーを用意する場合、ロードバランサー+Webサーバーという構成になる。
しかし、API Gatewayを利用することでロードバランサー+Webサーバーなどを用意する必要がなくなる
バックエンドの処理はAWS Lambda、既存のWebシステム、AWSのサービスが利用することができる

メリット
- インフラ環境のセットアップ
- インフラ環境の管理
などが不要になるため便利
```
#### APIの構成
|URL|HTTP Method|Process|Lambda Function|
|---|---|---|---|
|/images|Get|アップロードされている画像のURL一覧|getImages|
|/images|Post|画像の投稿|postImages|
|/images|Put|画像情報の更新|upsateImage|
|/images[id]|Get|指定したIDの画像URL取得|getImageById|
|/images[id]|Post|指定したIDの画像を削除|deleteImageById|

#### API実装前の準備
##### DynamoDBのテーブル作成
`aws dynamodb create-table --region ap-northeast-1 --table-name photos --attribute-definitions AttributeName=photo_id,AttributeType=S --key-schema AttributeName=photo_id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5`

```json
{
  "TableDescription": {
    "AttributeDefinitions": [
      {
        "AttributeName": "photo_id",
        "AttributeType": "S"
      }
    ],
    "TableName": "photos",
    "KeySchema": [
      {
        "AttributeName": "photo_id",
        "KeyType": "HASH"
      }
    ],
    "TableStatus": "CREATING",
    "CreationDateTime": "2020-04-19T12:24:34.200000+09:00",
    "ProvisionedThroughput": {
      "NumberOfDecreasesToday": 0,
      "ReadCapacityUnits": 5,
      "WriteCapacityUnits": 5
    },
    "TableSizeBytes": 0,
    "ItemCount": 0,
    "TableArn": "arn:aws:dynamodb:ap-northeast-1:618448440758:table/photos",
    "TableId": "112ad4ef-4d89-4aef-9071-986265bfda7a"
  }
}
```

##### 画像用S3バケットを準備

|backet name|memo|
|---|---|
|serverless-app-photos-vue|画像保存先|
|serverless-app-web-vue|静的ファイルの配信用|
|serverless-app-sam-vue|AWS SAMを利用したパッケージングで作成されたZIPパッケージが保存される場所(Lambda関数リリース用)|

###### backet作成
`aws s3 mb s3://serverless-app-photos-vue --region ap-northeast-1`
###### webホスティングを有効
`aws s3 website s3://serverless-app-photos-vue/ --index-document index.html`
###### アクセスポリシー作成
`aws s3api put-bucket-policy --bucket serverless-app-photos-vue --policy file://policy_photos-vue.json`

##### Lambda関数用のIAMロール作成
`aws iam create-role --role-name lambda-dynamodb-access --assume-role-policy-document file://trustpolicy.json`
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

##### DynamoDBアクセス権限付与をロールに付与
`aws iam put-role-policy --role-name lambda-dynamodb-access --policy-name dynamodb-access --policy-document file://permission.json`
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:DeleteItem",
        "dynamodb:GetItem",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:618448440758:table/photos"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::serverless-app-photos-vue/*"
    }
  ]
}
```

##### APIのバックエンド実装～リリース
`aws s3 mb s3://serverless-app-sam --region ap-northeast-1`

postImages.pyとtemplate.yamlを用意して下記コマンド実行
デプロイパッケージの作成
`aws cloudformation package --template-file template.yaml --output-template-file template-output.yaml --s3-bucket serverless-app-sam`

デプロイ
`aws cloudformation deploy --template-file template-output.yaml --stack-name serverless-app --capabilities CAPABILITY_IAM --region ap-northeast-1`

デプロイ後の確認
- Rest API一覧
`aws apigateway get-rest-apis --region ap-northeast-1`
- postImages
`curl -X POST https://<rest_api_id>.execute-api.ap-northeast-1.amazonaws.com/Prod/images -d '{"type":"image/jpeg", "size":1}'`
`curl -X POST https://idsz7xw2eh.execute-api.ap-northeast-1.amazonaws.com/Prod/images -d '{"type":"image/jpeg", "size":1}'`
- updateImage
`curl -X PUT https://<rest_api_id>.execute-api.ap-northeast-1.amazonaws.com/Prod/images -d '{"photo_id":"", "timestamp":1, "status":"Uploaded"}'`
`curl -X PUT https://idsz7xw2eh.execute-api.ap-northeast-1.amazonaws.com/Prod/images -d '{"photo_id":"173979f3-f2b5-4ebc-be98-368214d6be99", "timestamp":1587376502, "status":"Uploaded"}'`
- getImages
`curl -X GET https://<rest_api_id>.execute-api.ap-northeast-1.amazonaws.com/Prod/images`
`curl -X GET https://idsz7xw2eh.execute-api.ap-northeast-1.amazonaws.com/Prod/images`
- getImageById
`curl -X GET https://<rest_api_id>.execute-api.ap-northeast-1.amazonaws.com/Prod/images/[id]`
`curl -X GET https://idsz7xw2eh.execute-api.ap-northeast-1.amazonaws.com/Prod/images/173979f3-f2b5-4ebc-be98-368214d6be99`
- deleteImageById
`curl -X DELETE https://<rest_api_id>.execute-api.ap-northeast-1.amazonaws.com/Prod/images/[id]`
`curl -X DELETE https://idsz7xw2eh.execute-api.ap-northeast-1.amazonaws.com/Prod/images/173979f3-f2b5-4ebc-be98-368214d6be99`

##### フロント`serverlessapp`を参照
大きな注意点として、S3バケットに対してブラウザ上のJavascriptから直接ファイルをアップロードする場合、CORSの設定が必要になる
`aws s3api put-bucket-cors --bucket serverless-app-photos-vue --cors-configuration file://cors.json`
```json
// cors.json
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"] ,
      "AllowedMethods": ["GET", "PUT", "DELETE", "POST", "HEAD"] ,
      "AllowedOrigins": ["*"] ,
      "MaxAgeSeconds": 3000 
    }
  ]
}
```