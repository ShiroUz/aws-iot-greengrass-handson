import os
# ファイルの保存関数
def save(file_path: str, data):
    """Save file
    """
    # もし、ディレクトリが存在しない場合は作成する
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'wb') as f:
        f.write(data)

# ファイルの読み込み関数
def read(file_name: str) -> str:
    """Read file
    """
    with open(file_name, 'r') as f:
        return f.read()
