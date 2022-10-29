FROM python:3.11-alpine

RUN addgroup -g 9001 gitlab-vars
RUN adduser gitlab-vars -G gitlab-vars -u 9001 -D
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY util .
COPY requirements.txt .

RUN ln -s /usr/src/app/gitlab-vars-wrapper.sh /usr/local/bin/gitlab-vars

USER gitlab-vars