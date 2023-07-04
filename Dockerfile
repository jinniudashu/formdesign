FROM python:3.9
# FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y dos2unix # 如果基础镜像是 Debian 或 Ubuntu
# 给start.sh可执行权限
COPY ./start.sh /app/start.sh
RUN dos2unix /app/start.sh && chmod +x /app/start.sh

# 数据迁移，并使用uwsgi启动服务
ENTRYPOINT /bin/bash /app/start.sh