import json

# 例外クラスを拡張
class ExtendException(Exception):
    # https://qiita.com/Kept1994/items/26c60e6a5a4538e81adf
    def __init__(self, statusCode, description):
        self.statusCode = statusCode
        self.description = description

    def __str__(self):
        obj = {
            "statusCode": self.statusCode,
            "description": self.description
        }
        return json.dumps(obj)
