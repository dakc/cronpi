FROM python:3.6

RUN apt-get update -y && apt-get install vim cron git -y
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel twine

EXPOSE 22