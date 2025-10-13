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
$ cd ai-dp/lambda/ai-driving-partner/
$ sam build
$ sam deploy
```