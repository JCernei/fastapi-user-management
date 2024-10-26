FROM python:3.10-slim

# Install necessary dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    build-essential \
    pkg-config && \
    apt-get clean

WORKDIR /usr/src/app
ADD config.py .
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
