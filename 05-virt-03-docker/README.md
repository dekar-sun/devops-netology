## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

Создадим Dockerfile c содержимым:
```commandline
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ cat Dockerfile 
FROM nginx:1.21.5-alpine

## Replace the default nginx index page with our index.html file
RUN rm -rf /usr/share/nginx/html/*
COPY ./index.html /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]
```
В нём кроме index.html добавляется файл с настройками nginx. При этом nginx будет слушать порт 8080.
Содержимое nginx.conf:
```commandline
# Запускать в качестве менее привилегированного пользователя по соображениям безопасности..
user nginx;

# Значение auto устанавливает число максимально доступных ядер CPU,
# чтобы обеспечить лучшую производительность.
worker_processes    auto;

events { worker_connections 1024; }

http {
    server {
        # Hide nginx version information.
        server_tokens off;

        listen  8080;
        root    /usr/share/nginx/html;
        include /etc/nginx/mime.types;

        location / {
            try_files $uri $uri/ /index.html;
        }

        gzip            on;
        gzip_vary       on;
        gzip_http_version  1.0;
        gzip_comp_level 5;
        gzip_types
                        application/atom+xml
                        application/javascript
                        application/json
                        application/rss+xml
                        application/vnd.ms-fontobject
                        application/x-font-ttf
                        application/x-web-app-manifest+json
                        application/xhtml+xml
                        application/xml
                        font/opentype
                        image/svg+xml
                        image/x-icon
                        text/css
                        text/plain
                        text/x-component;
        gzip_proxied    no-cache no-store private expired auth;
        gzip_min_length 256;
        gunzip          on;
    }
}
```

Скачиваем необходимый образ nginx:
```commandline
dekar@Dekar-NIX:~$ docker pull nginx:1.21.5-alpine
1.21.5-alpine: Pulling from library/nginx
59bf1c3509f3: Pull complete 
f3322597df46: Pull complete 
d09cf91cabdc: Pull complete 
3a97535ac2ef: Pull complete 
919ade35f869: Pull complete 
40e5d2fe5bcd: Pull complete 
Digest: sha256:eb05700fe7baa6890b74278e39b66b2ed1326831f9ec3ed4bdc6361a4ac2f333
Status: Downloaded newer image for nginx:1.21.5-alpine
docker.io/library/nginx:1.21.5-alpine
```
Запускаем создание образа и проверяем доступные образа после этого:
```commandline
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ docker build -t deniskirianov/nginx:1.21.5 .
Sending build context to Docker daemon  5.632kB
Step 1/5 : FROM nginx:1.21.5-alpine
 ---> cc44224bfe20
Step 2/5 : RUN rm -rf /usr/share/nginx/html/*
 ---> Running in 6bb505028131
Removing intermediate container 6bb505028131
 ---> a90e5c72f1e7
Step 3/5 : COPY ./index.html /usr/share/nginx/html
 ---> 2a28c0744339
Step 4/5 : COPY ./nginx.conf /etc/nginx/nginx.conf
 ---> 7b96fcb6c96a
Step 5/5 : ENTRYPOINT ["nginx", "-g", "daemon off;"]
 ---> Running in 50f350745971
Removing intermediate container 50f350745971
 ---> 839d98d17d19
Successfully built 839d98d17d19
Successfully tagged deniskirianov/nginx:1.21.5
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ docker images
REPOSITORY            TAG             IMAGE ID       CREATED          SIZE
deniskirianov/nginx   1.21.5          839d98d17d19   13 seconds ago   23.5MB
nginx                 1.21.5-alpine   cc44224bfe20   3 weeks ago      23.5MB
```
Запускаем контейнер из собранного образа и проверяем доступность html странички:
```commandline
dekar@Dekar-NIX:~$ docker run -d -p 80:8080 --name nginx 839d98d17d19
23432687396f4a84774a4a8467eb4b23a7fa0d99be15930becd5958c4860b010
dekar@Dekar-NIX:~$ curl -v 127.0.0.1
*   Trying 127.0.0.1:80...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 80 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx
< Date: Tue, 25 Jan 2022 11:55:29 GMT
< Content-Type: text/html
< Content-Length: 90
< Last-Modified: Tue, 25 Jan 2022 11:23:55 GMT
< Connection: keep-alive
< ETag: "61efddcb-5a"
< Accept-Ranges: bytes
< 
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
* Connection #0 to host 127.0.0.1 left intact
```
Пушим образ в удалённый репозиторий:
```commandline
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ docker login -u deniskirianov
Password: 
WARNING! Your password will be stored unencrypted in /home/dekar/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
dekar@Dekar-NIX:~/DevOps/netology_hw/05-virt-03-docker/Docker#1$ docker push deniskirianov/nginx:1.21.5
The push refers to repository [docker.io/deniskirianov/nginx]
b326fddbaf3d: Pushed 
5f163266cae8: Pushed 
33038e696ae6: Pushed 
419df8b60032: Mounted from library/nginx 
0e835d02c1b5: Mounted from library/nginx 
5ee3266a70bd: Mounted from library/nginx 
3f87f0a06073: Mounted from library/nginx 
1c9c1e42aafa: Mounted from library/nginx 
8d3ac3489996: Mounted from library/nginx 
1.21.5: digest: sha256:8d29e72e787e8a563f6be203b7f7897bbca794d411fc43b1e9869e73180f23b9 size: 2189
```
Образ доступен по адресу: https://hub.docker.com/r/deniskirianov/nginx

## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
  - В зависимости от степени нагруженности может подойти физическая машина или виртуальная. Т.к. приложение монолитное, то Docker тут не подходит.
- Nodejs веб-приложение;
  - Для таких приложений достаточно Docker, т.к. они хорошо работают в контейнерах.
- Мобильное приложение c версиями для Android и iOS;
  - Скорее всего такое приложение необходимо запускать на виртуальной машине, т.к. ему необходим GUI, который не поддерживается dockerом.
- Шина данных на базе Apache Kafka;
  - Виртуальная машина. Т.к. в продакшене эта высоконагруженная система. Для тестирования, думаю, подойдёт докер контейнер.
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
  - Ноды Elasticsearch лучше разворачивать на виртуальных машинах, при этом отказоустойчивость осуществляется кластером.
    При этом logstash и kibana можно развернуть в docker контейнерах, если устроит производительность.
- Мониторинг-стек на базе Prometheus и Grafana;
  - Системы не хранят в себе данных (метрик), так, что, можно развернуть в Docker.   
- MongoDB, как основное хранилище данных для java-приложения;
  - Виртуальная машина, т.к. хранить данные в контейнере плохая практика.
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.
  - Скорее всего подойдет виртуальная машина, т.к. необходимо хранить большие данные для Docker Registry.
    Для Gitlab, в некоторых кейсах, подойдёт docker контейнер с примонтированным volume для хранения настроек, плагинов и пайплайнов.

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.

Создаём каталог data и запускаем два контейнера с подключенной папкой data:
```commandline
dekar@Dekar-NIX:~$ mkdir ~/data
dekar@Dekar-NIX:~$ docker run -d -it --rm  --name centos -v ~/data://data centos
af289038290840a5de6d713f9500afc8cb3a9422ebaba72732298199491a6042
dekar@Dekar-NIX:~$ docker run -d -it --rm  --name debian -v ~/data://data debian
660dde7a2575cc100ee9aea5a56ed3ff50ddc5088e97fea43ac533e81a95d9e2
dekar@Dekar-NIX:~$ docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
660dde7a2575   debian    "bash"        3 seconds ago    Up 1 second               debian
af2890382908   centos    "/bin/bash"   52 seconds ago   Up 51 seconds             centos
```
Подключаемся к контейнеру с centos и создаём текстовый файл:
```commandline
dekar@Dekar-NIX:~$ docker exec -it centos /bin/bash
[root@af2890382908 /]# cd /data
[root@af2890382908 data]# vi file.txt
[root@af2890382908 data]# cat file.txt
Hello Netology!!!
```

Создаём на хостовой машине дополнительный файл в каталоге ~/data:
```commandline
dekar@Dekar-NIX:~$ cd ~/data/
dekar@Dekar-NIX:~/data$ ll
total 12
drwxrwxr-x  2 dekar dekar 4096 янв 25 15:14 ./
drwxr-xr-x 39 dekar dekar 4096 янв 25 15:01 ../
-rw-r--r--  1 root  root    18 янв 25 15:14 file.txt
dekar@Dekar-NIX:~/data$ vim other_file.txt
dekar@Dekar-NIX:~/data$ cat other_file.txt
Hello World!!!
```
Подключаемся во второй контейнер на базе debian и проверяем созданные файлы:
```commandline
dekar@Dekar-NIX:~/data$ docker exec -it debian /bin/bash
root@660dde7a2575:/# cd /data/
root@660dde7a2575:/data# ls -la
total 16
drwxrwxr-x 2 1000 1000 4096 Jan 25 12:16 .
drwxr-xr-x 1 root root 4096 Jan 25 12:12 ..
-rw-r--r-- 1 root root   18 Jan 25 12:14 file.txt
-rw-rw-r-- 1 1000 1000   15 Jan 25 12:16 other_file.txt
root@660dde7a2575:/data# cat file.txt 
Hello Netology!!!
root@660dde7a2575:/data# cat other_file.txt 
Hello World!!!
```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.

Ссылка на собранный образ: https://hub.docker.com/r/deniskirianov/ansible

