import os
# ファイルの保存関数
def save(file_name: str, data):
    """Save file
    """
    tmp_path = os.path.join('/tmp', file_name)
    with open(tmp_path, 'wb') as f:
        f.write(data)
    return tmp_path

# ファイルの読み込み関数
def read(file_name: str) -> str:
    """Read file
    """
    with open(file_name, 'r') as f:
        return f.read()
