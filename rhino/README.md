
# 项目环境配置说明

## 开发环境

提供给开发人员进行程序/功能开发测试使用的环境。

* 分支:develop
* 分支:feature/monitor

## rhino介绍

帐号/密码：向linshirong申请

## 技术与工具

### 主要技术

* Python 3.5+
* Django
* Django REST framework
* Mysql
* VUE

### 工具

* Pycharm

# 环境搭建步骤
### 1.安装python包
pip install -r requirements.txt

### 安装confluent-kafka需要先安装librdkafka组件
librdkafka is embedded in the manylinux wheels, for other platforms or when a specific version of librdkafka is desired, following these guidelines:
* For Debian/Ubuntu** based systems, add this APT repo and then do sudo apt-get install librdkafka-dev python-dev: http://docs.confluent.io/current/installation.html#installation-apt
* For RedHat and RPM-based distros, add this YUM repo and then do sudo yum install librdkafka-devel python-devel: http://docs.confluent.io/current/installation.html#rpm-packages-via-yum
* On OSX, use homebrew and do sudo brew install librdkafka

### 2.从git上获取rhino
git clone -b feature/monitor git@10.1.1.11:linshirong/rhino.git

### 3.启动rhino
python manage.py runserver 0.0.0.0:1314

### 4. 启动flower
flower  --port=5555 --broker=redis://localhost:6379/0

### 5. 启动celery
celery worker -A rhino -l info

### 6. 启动beat
celery -A rhino beat -l info

配置文件更新
rhino.ini配置pyspider的task数据库
数据库更新

### 7. 下载配置nginx
```
 wget http://downloads.sourceforge.net/project/pcre/pcre/8.35/pcre-8.35.tar.gz
 tar zxvf pcre-8.35.tar.gz
 cd pcre-8.35
 ./configure
 make && make install
```
```
wget http://nginx.org/download/nginx-1.12.2.tar.gz
tar zxvf nginx-1.12.2.tar.gz
cd nginx-1.12.2
./configure --prefix=/usr/local/nginx --with-zlib=../zlib-1.2.8 --with-pcre=../pcre-8.36
make
sudo make install
```
### 8. 启动nginx
nginx -s start


__添加 /etc/nginx/nginx.conf__  
```include /etc/nginx/rhino.conf;```


__rhino.config的配置文件__
```
server {
        listen 8000;
	server_name 0.0.0.0;
	root /home/maybe/VUErhino;

        # access_log /var/log/testwx.log main;

        #处理vue-router路径Start
        #如果找不到路径则跳转到@router变量中寻找,找到了就默认进入index.html
        location /monitor2 {


             index index.html;
             try_files $uri $uri/ /monitor2/index.html;
             index index.html;
         }

	location / {
		proxy_pass http://localhost:1314;
	}
        #处理vue-router路径End

}
```

__测试配置文件__  
nginx -t

### 重新启动nginx
nginx -s  reload

## 数据上线
### 修改数据库
python3 manage.py makemigrations
python3 manage.py migrate
新添加一个记录报警的数据库  
crawler添加了source, url等字段  
project添加了es_table(记录es地址)等字段  

### 补充数据  
通过python程序和excel表中的对应关系补充crawler数据库的source, url  
通过sql文件添加project对应es存入路径




__访问127.0.0.1:8000/monitor2__
