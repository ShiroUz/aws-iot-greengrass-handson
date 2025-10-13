ARG AWS_ACCOUNT_ID
FROM ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/aws-gg-handson/ai-dp/arm32v7/python:v3.12.10 AS builder

# Set environment variables to avoid GStreamer warnings
ENV OPENCV_VIDEOIO_PRIORITY_MSMF=0
ENV OPENCV_VIDEOIO_DEBUG=1

WORKDIR /app
COPY src/ ./src/
COPY main.py .

# For Test
COPY Kurzweil-K2000-Dual-Bass-C1.wav .

CMD ["python3", "-u", "main.py"]