FROM python:3.9
# FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk add --update alpine-sdk
# RUN apk add --update --no-cache postgresql-client jpeg-dev

# RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev build-base python3-dev libffi-dev openssl-dev cargo

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN apk del .tmp-build-deps

COPY . /app/

# Expose the port uWSGI will listen on
EXPOSE 8000

# Run uWSGI
CMD ["uwsgi", "--ini", "formdesign_uwsgi.ini"]