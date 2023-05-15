FROM ubuntu:latest
# FROM python:3.9
LABEL Hyeongseok Choi <hschoi9209@google.com> 
LABEL env="1.0"
# debugging
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y vim net-tools
RUN apt-get install -y git
RUN apt-get install fonts-nanum*

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

COPY requirements.txt .

# install python dependencies
RUN apt-get update
RUN apt-get install -y python3-dev build-essential python3 python3-pip python3-venv
RUN pip3 install --upgrade pip

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY env.sample .env

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
