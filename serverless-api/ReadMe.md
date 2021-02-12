1. プロジェクト作成
```
chalice new-project <project_name>
```

2. プロジェクトデプロイ
```
# AWSデプロイ
chalice deploy --stage <stage_name>

# ローカル実行
`chalice local --stage dev`

# AWS削除
`chalice delete --stage <stage_name>`
```

3. DynamoDBをシミュレートして初期データの登録
    1. DynamoDB Local起動
    
    `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8001`

    2. スキーマ作成

    `aws dynamodb create-table --cli-input-json file://etc/schema-images.json --endpoint-url http://localhost:8001`
    `aws dynamodb create-table --cli-input-json file://etc/schema-videos.json --endpoint-url http://localhost:8001`

    3. 初期データ投入

    `aws dynamodb batch-write-item --request-items file://etc/initial-data-images.json --endpoint-url http://localhost:8001`
    `aws dynamodb batch-write-item --request-items file://etc/initial-data-videos.json --endpoint-url http://localhost:8001`

    3. 初期データ確認

    `aws dynamodb scan --table-name Images --endpoint-url http://localhost:8001`

(DynamoDB Local)[https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html]

4. API呼び出し
```bash
curl -X GET http://localhost:8000/videos
curl -X POST http://localhost:8000/videos -d '{"title":"hogehoge1","type":"video/mp4", "size":1}' -H "Content-Type:application/json"
curl -X PUT http://localhost:8000/videos/cd2d678679954ea6b4a094b00efbc595 -d '{"title":"hogehoge2"}' -H "Content-Type:application/json"
curl -X GET http://localhost:8000/videos/cd2d678679954ea6b4a094b00efbc595
curl -X DELETE http://localhost:8000/videos/hogehoge2
```