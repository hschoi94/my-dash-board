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
//내부ip(localhost) 접속 가능 계정
//외부ip 접속 가능 계정
CREATE USER 계정아이디@HOST IDENTIFIED BY 비밀번호;
```
여기에서 HOST에 % 표시는 어느곳이나 접근이 가능하다는 의미이다.

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