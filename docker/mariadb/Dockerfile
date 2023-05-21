FROM mariadb:latest

LABEL Hyeongseok Choi <hschoi9209@gmail.com> 
RUN mkdir /sql
WORKDIR /sql

# COPY ./sql .
# RUN mkdir /docker-entrypoint-initdb.d
COPY ./sql/* /docker-entrypoint-initdb.d
CMD ["mysqld"]
# CMD [ "mysql", "-u root -p root < /sql/test.sql" ]
# https://emunhi.com/view/201812/02154627862?menuNo=10031
# https://mycup.tistory.com/382