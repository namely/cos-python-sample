FROM python:3.7.6-stretch

WORKDIR /app/

# install dependencies
ADD ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

# add code
ADD ./server/ /app/server/
WORKDIR /app/server
