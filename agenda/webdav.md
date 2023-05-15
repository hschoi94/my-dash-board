# webdav

``` bash
# webdav 
sudo apt install apache2 apache2-utils

# webdav activate
sudo a2enmod dav
sudo a2enmod dav_fs
sudo service apache2 restart

# autoindex를 비활성화 했을 경우 활성화
# autoindex는 디렉토리 내용을 리스트로 보여주는 모듈이라 서버 보안에는 좋지 않기에 비활성화 했던것이 문제
sudo a2enmod autoindex

# 모듈 활성화 후 webdav의 경로로 사용할 디렉토리 선택 
# apache 기본 경로에 webdav용 폴더 생성
sudo mkdir /var/www/html/webdav

# webdav에 사용할 폴더 소유권자 변경
sudo chown www-data /var/www/html/webdav

# 패스워드 파일 새로 생성
sudo htpasswd -c /etc/apache2/webdav.password 사용자이름

# 외부에서 수정할 수 없게 권한 설정
sudo chmod 640 /etc/apache2/webdav.password

# apache에서 password 파일에 접근 가능하게 소유자 변경
sudo chown root:www-data /etc/apache2/webdav.password
```

``` sh
# /etc/apache2/sites-available/000-default.conf

# <VirtualHost :80> 태그 안에 아래 내용 작성
# Alias '사용할 이름' '접근할 디렉토리 경로'
Alias /webdav /var/www/html/webdav
<Location /webdav>
	DAV on
	AuthType Basic
	AuthName "webdav"
	AuthUserFile /etc/apache2/webdav.password
	Require valid-user
</Location>
<Directory /var/www/html/webdav>
	DAV on
	Options Indexes FollowSymLinks MultiViews
	AllowOverride all
	Order allow,deny
	allow from all
</Directory>
```
sudo service apache2 restart