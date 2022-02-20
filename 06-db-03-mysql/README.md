# Домашнее задание к занятию "6.3. MySQL"

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

В следующих заданиях мы будем продолжать работу с данным контейнером.

#### Скачиваем и запускаем докер образ с mysql 8:
```commandline
dekar@Dekar-NIX:~$ docker pull mysql:8.0
8.0: Pulling from library/mysql
6552179c3509: Pull complete 
d69aa66e4482: Pull complete 
3b19465b002b: Pull complete 
7b0d0cfe99a1: Pull complete 
9ccd5a5c8987: Pull complete 
2dab00d7d232: Pull complete 
5d726bac08ea: Pull complete 
11bb049c7b94: Pull complete 
7fcdd679c458: Pull complete 
11585aaf4aad: Pull complete 
5b5dc265cb1d: Pull complete 
fd400d64ffec: Pull complete 
Digest: sha256:e3358f55ea2b0cd432685d7e3c79a33a85c7a359b35fa87fc4993514b9573446
Status: Downloaded newer image for mysql:8.0
docker.io/library/mysql:8.0
dekar@Dekar-NIX:~$ docker volume create vol_mysql
vol_mysql
dekar@Dekar-NIX:~$ docker run --name mysql8 -e MYSQL_ROOT_PASSWORD=Qwerty12345 --rm -d -p 3306:3306 -v vol_mysql:/etc/mysql/ -v vol_backup:/backup mysql:8.0
866cde7e8a3bbe79bb02c56016e9ad099aca0e0eec2982a80ed301841b4717a0
```

#### Восстанавливаем базу из бэкапа (бэкап был предварительно скопирован в vol_backup):
```commandline
dekar@Dekar-NIX:~$ docker exec -it mysql8 mysql -pQwerty12345 -e 'CREATE DATABASE test_db;'
mysql: [Warning] Using a password on the command line interface can be insecure.
dekar@Dekar-NIX:~$ docker exec -it mysql8 mysql -pQwerty12345 -e 'source /backup/test_dump.sql' test_db
mysql: [Warning] Using a password on the command line interface can be insecure.
```

#### Подключаемся к базе:
```commandline
dekar@Dekar-NIX:~$ mysql -u root -h 127.0.0.1 -pQwerty12345
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

#### Статус базы:
```commandline
mysql> USE test_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> \s
--------------
mysql  Ver 8.0.28-0ubuntu0.20.04.3 for Linux on x86_64 ((Ubuntu))

Connection id:          12
Current database:       test_db
Current user:           root@172.17.0.1
SSL:                    Cipher in use is TLS_AES_256_GCM_SHA384
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         8.0.28 MySQL Community Server - GPL
Protocol version:       10
Connection:             127.0.0.1 via TCP/IP
Server characterset:    utf8mb4
Db     characterset:    utf8mb4
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
TCP port:               3306
Binary data as:         Hexadecimal
Uptime:                 59 min 42 sec

Threads: 5  Questions: 174  Slow queries: 0  Opens: 194  Flush tables: 3  Open tables: 112  Queries per second avg: 0.048
--------------
```

#### Список таблий test_db:
```commandline
mysql> SHOW TABLES;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0,01 sec)
```

#### Количество записей с `price` > 300.
```commandline
mysql> SELECT COUNT(*) FROM orders WHERE price >300;
+----------+
| count(*) |
+----------+
|        1 |
+----------+
1 row in set (0,00 sec)
```


## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

#### Создаём пользователя:
```commandline
mysql> CREATE USER 'test'@'localhost' IDENTIFIED BY 'test-pass';
Query OK, 0 rows affected (0,03 sec)

mysql> ALTER USER 'test'@'localhost' ATTRIBUTE '{"fname":"James", "lname":"Pretty"}';
Query OK, 0 rows affected (0,02 sec)

mysql> ALTER USER 'test'@'localhost' WITH MAX_QUERIES_PER_HOUR 100 PASSWORD EXPIRE INTERVAL 180 DAY FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2;
Query OK, 0 rows affected (0,03 sec)
```

#### Предоставляем привелегии:
```commandline
mysql> GRANT SELECT ON test_db.orders TO 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0,02 sec)
```

#### Данные пользователя test:
```commandline
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER='test';
+------+-----------+---------------------------------------+
| USER | HOST      | ATTRIBUTE                             |
+------+-----------+---------------------------------------+
| test | localhost | {"fname": "James", "lname": "Pretty"} |
+------+-----------+---------------------------------------+
1 row in set (0,01 sec)
```

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`

#### Устанавливаем профилирование:
```commandline
mysql> SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0,00 sec)
```

Проверяем текущий `engine`:
```commandline
mysql> SELECT TABLE_NAME,ENGINE,TABLE_ROWS,DATA_LENGTH,INDEX_LENGTH FROM information_schema.TABLES WHERE table_name = 'orders' and  TABLE_SCHEMA = 'test_db';+------------+--------+------------+-------------+--------------+
| TABLE_NAME | ENGINE | TABLE_ROWS | DATA_LENGTH | INDEX_LENGTH |
+------------+--------+------------+-------------+--------------+
| orders     | InnoDB |          5 |       16384 |            0 |
+------------+--------+------------+-------------+--------------+
1 row in set (0,00 sec)
```

#### Меняем `engine` на MyISAM:
```commandline
mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0,28 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

#### Переключаем `engine` обратно:
```commandline
mysql> ALTER TABLE orders ENGINE = InnoDB;
Query OK, 5 rows affected (0,41 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

Вывод `SHOW PROFILES;`:
```commandline
mysql> SHOW PROFILES;
+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                                                                                            |
+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        2 | 0.00270175 | SELECT TABLE_NAME,ENGINE,TABLE_ROWS,DATA_LENGTH,INDEX_LENGTH FROM information_schema.TABLES WHERE table_name = 'orders' and  TABLE_SCHEMA = 'test_db'            |
|        3 | 0.27781675 | ALTER TABLE orders ENGINE = MyISAM                                                                                                                               |
|        4 | 0.41577800 | ALTER TABLE orders ENGINE = InnoDB                                                                                                                               |
+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
Видим, что переключение на InnoDB заняло больше времени, чем на MyISAM.

## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

#### Смотрим содержимое файла my.cnf:
```commandline
dekar@Dekar-NIX:~$ docker exec -it mysql8 cat /etc/mysql/my.cnf
# Copyright (c) 2017, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

#
# The MySQL  Server configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/
```
#### Создаём backup файла my.cnf:
```commandline
dekar@Dekar-NIX:~$ docker exec -it mysql8 cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak
dekar@Dekar-NIX:~$ docker exec -it mysql8 ls -la /etc/mysql
total 24
drwxr-xr-x 3 root root 4096 Feb 20 18:49 .
drwxr-xr-x 1 root root 4096 Feb 20 17:01 ..
drwxrwxr-x 2 root root 4096 Feb 20 17:01 conf.d
-rw-rw-r-- 1 root root 1080 Feb 18 01:23 my.cnf
-rw-r--r-- 1 root root 1080 Feb 20 18:49 my.cnf.bak
-rw-r--r-- 1 root root 1448 Dec 17 16:39 my.cnf.fallback
```

#### Подключаемя к контейнеру и пишем необходимые настройки в my.cnf:
```commandline
dekar@Dekar-NIX:~$ docker exec -it mysql8 bash
root@866cde7e8a3b:/# cat << EOF >> /etc/mysql/my.cnf
> innodb_flush_log_at_trx_commit = 2
> innodb_file_format             = Barracuda
> innodb_log_buffer_size         = 1M
> innodb_buffer_pool_size        = 4915М
> innodb_log_file_size           = 100M
> EOF
root@866cde7e8a3b:/# more /etc/mysql/my.cnf
# Copyright (c) 2017, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

#
# The MySQL  Server configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/
innodb_flush_log_at_trx_commit = 2
innodb_file_format             = Barracuda
innodb_log_buffer_size         = 1M
innodb_buffer_pool_size        = 4915М
innodb_log_file_size           = 100M
```