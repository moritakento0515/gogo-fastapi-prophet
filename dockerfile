FROM python:3.10-slim

WORKDIR /app

# 依存関係のコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI アプリのコードをコピー（srcフォルダなど）
COPY ./src /app/src

# models フォルダをコンテナにコピー
COPY ./models /app/models

# FastAPI アプリの起動
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
