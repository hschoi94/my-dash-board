# Database

## database root 권한

root 계정의 경우 관리자 계정이기 때문에 데이터베이스의 모든 권한을 가진다. 따라서 이 root 권한을 획득하게 된다면 아무나 데이터베이스(DB)안의 자료를 생성, 조회, 수정이 가능하다.

이는 보안상의 문제나 실수에 의해 자료가 조작될 수 있음을 의미하고, 이를 방지하기 위해 DB 사용자들에게 용도에 맞는 권한을 부여하는 계정을 부여하여 문제를 사전에 방지하는 것이 일반적이다. (root 계정을 마음대로 사용하지 않는다.)

mariadb에서 root host을 설정하지 않는다면 localhost에서만 접근이 가능하며 원격으로는 접근하지 못하는 상태가 된다.

MariaDB가 실행중인 컴퓨터의 터미널에서 아래의 명령어로 접속이 가능하다.

``` bash
> mysql -u root -p
Enter password: # 설정한 비밀번호 입력
```

따라서 sql 계정을 아래의 SQL 구문으로 생성할 수 있다.

``` sql
CREATE USER 계정아이디@HOST IDENTIFIED BY 비밀번호;
```

여기에서 HOST에 % 을 기입하면 어느곳이나 접근이 가능하다는 의미이다.

그리고 DB을 생성하고 생성한 DB에 계정마다 권한을 부여한다.

```sql
// DB 생성
CREATE DATABASE 데이터베이스이름

// 권한 부여
GRANT 권한 ON 데이터베이스명.* TO 계정아이디@호스트;
//권한 적용
FLUSH PRIVILEGES;

//권한 부여 확인
SHOW GRANTS FOR 계정아이디@호스트;
```

[실행된 query 확인](https://wildeveloperetrain.tistory.com/229)
[SQL 최적화](https://wildeveloperetrain.tistory.com/203)

## MariaDB 데이터 베이스 세팅

[MariaDB docker image 공식 문서](https://hub.docker.com/_/mariadb)에 따르면 '/docker-entrypoint-initdb.d'에 .sql 파일을 넣으면 자동적으로 instance을 생성 가능하다고 함

sql file의 존재를 알고 아래의 코드를 수행한 뒤, sql 파일로 설정 동작 확인

- sql file을 사용하는 과정에서 dockerfile에 COPY로 파일 넣기, docker-compose.yml에서 -v 을 이용하여 파일 넣기

``` bash
mysql -u root -p # mysql 접속
source <sql file path>
```

- 시도 결과 단순히 'mariaDB' /docker-entrypoint-initdb.d 에 입력했을 때, 정상적으로 설정되지 않음.

- [MARIADB_USER을 설정하면 될 수 있다는 게시글](https://stackoverflow.com/questions/62922399/을docker-compose-mariadb-docker-entrypoint-initdb-d-sql-is-not-executed)을 적용했을 때에도 동작하지 않음
  - windows에서는 root로 했을 때, 동작했지만 mac에서는 동작하지 않는다고 함.
  - MARIADB_USER는 새로운 USER을 등록하는 것이 아니라 내부 사용자를 지정하는 것이 아닐까?
    - 공식문서에 따르면 새로운 USER을 생성하는 것으로 MARIADB_PASSWORD 옵션으로 비밀번호까지 설정 그리고 이 계정은 MARIADB_DATABASE로 설정된 DB에 대하여 GRANT ALL로 모든 권한을 가짐

[Database만 여러개 만들 수 있을까?](https://stackoverflow.com/questions/50173296/multiple-mariadb-databases-in-docker)
Database을 여러개 만들지 않고 Table만 여러개 만들면되지 않을까?
- 내가 생각하기에는 Database가 여러개일 필요가 없어 보인다. [관련된 글](https://okky.kr/questions/844821)에서 약간의 설명을 해준다.

- 그렇다면 Table만 생성하는 것은 가능한가?