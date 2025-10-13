ARG AWS_ACCOUNT_ID
FROM ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/aws-gg-handson/wc-led/arm32v7/python:v3.12.10 AS builder

WORKDIR /app
COPY src/ ./src/
COPY main.py .
COPY Kurzweil-K2000-Dual-Bass-C1.wav .

CMD ["python", "-u", "main.py", "World"]
