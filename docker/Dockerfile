FROM python:3.6

RUN apt-get update -y && apt-get install vim cron git tzdata -y
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel twine
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

EXPOSE 22