FROM python:3.8

RUN mkdir /app
COPY . /app 
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt -i https://pypi.douban.com/simple
WORKDIR /app