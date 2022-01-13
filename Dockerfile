#Django-meetups-rest build. see readme.MD for setup and environment variables. 
FROM python:slim-bullseye

ENV PYTHONUNBUFFERED 1 

RUN mkdir /code
COPY . /code
WORKDIR /code

#COPY ./requirements.txt .

RUN apt update \ 
	&& apt install -y python3-dev build-essential python3-pip default-libmysqlclient-dev vim\ 
	&& pip3 install --no-cache-dir -r requirements.txt \
	&& apt-get purge -y  \
	&& pip3 install --upgrade pip \ 
	&& pip3 install -r requirements.txt




