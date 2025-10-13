# Lambda

## Layerの作成
```
$ pyenv local ${python version}
$ pyenv glocal ${python version}
$ poetry update
$ poetry export --format requirements.txt -o ../layer/requirements.txt --without-hashes
$ cd ../layer
$ pip3 install -r requirements.txt -t ./python/
$ zip -r python.zip python
```

## SAM Deploy

```
$ cd wc-led/lambda/put-device-address/
$ sam build
$ sam deploy
```

## Testイベントで住所登録する方法
```json
{
  "httpMethod": "POST",
  "body": "{\"ThingId\": \"dev-aws-gg-handson-wc-led-0-thing\", \"UserId\": \"d6ce24d7-2188-42dd-8cb6-4364e96a9ec9\", \"UserName\": \"ShiroUz\", \"Address\": \"東京都〇〇区××\"}"
}
```