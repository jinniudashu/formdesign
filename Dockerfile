FROM python:3.9
# FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

# 给start.sh可执行权限
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh
RUN ls -la /app
# 数据迁移，并使用uwsgi启动服务
ENTRYPOINT /bin/bash /app/start.sh