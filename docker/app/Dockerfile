FROM ubuntu:latest

LABEL Hyeongseok Choi <hschoi9209@gmail.com> 
LABEL env="1.0"

# debugging
RUN apt-get update
RUN apt-get install -y vim net-tools
RUN apt-get install -y git
RUN apt-get install fonts-nanum*

COPY requirements.txt .

# install python dependencies
RUN apt update
RUN apt-get install -y python3-dev build-essential python3 python3-pip python3-venv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN git clone https://github.com/hschoi94/my-dash-board.git 
RUN cd /my-dash-board
RUN git checkout exp
# RUN mkdir -p /var/www/html/webdav

# # 관리하는 초기 파일들을 migrations라는 디렉터리에 자동으로 생성
# # 우리는 우리가 진행할 프로젝트에서 flask 실행을 맡을 main app(python file)을 만들어주어서
# # 환경설정에 FLASK_APP으로 지정해주어야한다.
# # ENV FLASK_APP=./run.py
# # RUN flask db init

# # RUN mkdir -p ./apps/migration
# # RUN flask db migrate -m "Initial migration."
# # RUN flask db migrate
# # RUN flask db upgrade

# # gunicorn
# # CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
