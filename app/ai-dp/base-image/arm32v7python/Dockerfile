FROM arm32v7/python:3.11.13-slim-bookworm AS builder

# Set environment variables(apt installでpython3-opencvを入れるため)
ENV PYTHONPATH=/usr/lib/python3/dist-packages

RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    gcc \
    g++ \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-gpiozero \
    vim \
    wget \
    alsa-utils \
    mpg321 \
    # OpenCV dependencies
    # libsm6 \
    # libxext6 \
    # libxrender-dev \
    # libgl1-mesa-glx \
    # libglib2.0-0 
    # pip installだとbuild時間が長すぎたのでシステムに入れる
    python3-opencv \
    # libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Create directories for storing images and audio
RUN mkdir -p /app/images /app/audio
