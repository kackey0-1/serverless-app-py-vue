1. プロジェクト作成
```
chalice new-project <project_name>
```

2. プロジェクトデプロイ
```
# AWSデプロイ
chalice deploy local --stage devORprod

# ローカル実行
`chalice local --stage dev`

# AWS削除
chalice delete --stage devORprod
```

3. DynamoDBをシミュレートして初期データの登録
    1. DynamoDB Local起動
    
    `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8001`

    2. スキーマ作成

    `aws dynamodb create-table --cli-input-json file://etc/schema.json --endpoint-url http://localhost:8001`

    3. 初期データ投入

    `aws dynamodb batch-write-item --request-items file://etc/initial-data.json --endpoint-url http://localhost:8001`

    3. 初期データ確認

    `aws dynamodb scan --table-name Images --endpoint-url http://localhost:8001`

(DynamoDB Local)[https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html]

4. 