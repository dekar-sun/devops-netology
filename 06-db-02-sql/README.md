# Домашнее задание к занятию "6.2. SQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.
Приведите получившуюся команду или docker-compose манифест.

#### Скачиваем PostgreSQL 12ой версии и создаём 2 volumes:

```commandline
dekar@Dekar-NIX:~/tmp$ docker pull postgres:12
12: Pulling from library/postgres
5eb5b503b376: Pull complete 
daa0467a6c48: Pull complete 
7cf625de49ef: Pull complete 
bb8afcc973b2: Pull complete 
c74bf40d29ee: Pull complete 
2ceaf201bb22: Pull complete 
1255f255c0eb: Pull complete 
12a9879c7aa1: Pull complete 
f7ca80cc6dd3: Pull complete 
6714db455645: Pull complete 
ee4f5626bf60: Pull complete 
621bb0c2ae77: Pull complete 
a19e980f0a72: Pull complete 
Digest: sha256:505d023f030cdea84a42d580c2a4a0e17bbb3e91c30b2aea9c02f2dfb10325ba
Status: Downloaded newer image for postgres:12
docker.io/library/postgres:12
dekar@Dekar-NIX:~/tmp$ docker volume create vol_db
vol_db
docker volume create vol_backup
vol_backup
dekar@Dekar-NIX:~/tmp$ docker volume ls
DRIVER    VOLUME NAME
local     vol_backup
local     vol_db
```
#### Запускаем контейнер:
```commandline
dekar@Dekar-NIX:~/tmp$ docker run --name postgres12 -e POSTGRES_PASSWORD=Qwerty12345 --rm -d -p 5432:5432 -v vol_db:/var/lib/postgresql/data -v vol_backup:/backup postgres:12
68ca4e81e48a2b4a89db379b6193c2b94c50c69607be4d869917fdcf9311f585
```
#### Проверяем:
```commandline
dekar@Dekar-NIX:~/tmp$ docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED              STATUS          PORTS                                       NAMES
68ca4e81e48a   postgres:12   "docker-entrypoint.s…"   About a minute ago   Up 59 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres12
```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

#### Подключаемся к базе:
```commandline
dekar@Dekar-NIX:~$ psql --host=127.0.0.1 --port=5432 --username=postgres
Password for user postgres: 
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 12.10 (Debian 12.10-1.pgdg110+1))
Type "help" for help.

postgres=#
```
#### Создаем пользователя test-admin-user и БД test_db:
```commandline
postgres=# CREATE DATABASE test_db;
CREATE DATABASE
postgres=# CREATE ROLE "test-admin-user";
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE test_db TO "test-admin-user";
GRANT
test_db=# GRANT USAGE, CREATE ON SCHEMA public TO "test-admin-user";
GRANT
test_db=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "test-admin-user";
GRANT
```

#### Проверяем:
```commandline
postgres=# \l
                                     List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |       Access privileges        
-----------+----------+----------+------------+------------+--------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                  +
           |          |          |            |            | postgres=CTc/postgres         +
           |          |          |            |            | "test-admin-user"=CTc/postgres
(4 rows)
```

#### Создаем таблицы:
```commandline
postgres=# \c test_db
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 12.10 (Debian 12.10-1.pgdg110+1))
You are now connected to database "test_db" as user "postgres".
test_db=# CREATE TABLE orders (id integer PRIMARY KEY, name text, price integer);
CREATE TABLE
test_db=# CREATE TABLE clients (id integer PRIMARY KEY, lastname text, country text, zakaz integer, FOREIGN KEY (zakaz) REFERENCES orders (Id));
CREATE TABLE
```

#### Создадим index для столбца country:
```commandline
test_db=# CREATE INDEX country_idx ON clients(country); 
CREATE INDEX
```

#### Создаем пользователя test-simple-user и выдаём ему права на таблицы orders и clients на SELECT/INSERT/UPDATE/DELETE:
```commandline
postgres=# CREATE ROLE "test-simple-user";
CREATE ROLE
postgres=# GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE public.clients TO "test-simple-user";
GRANT
test_db=# GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE public.orders TO "test-simple-user";
GRANT
test_db=# \dp
                                     Access privileges
 Schema |  Name   | Type  |        Access privileges         | Column privileges | Policies 
--------+---------+-------+----------------------------------+-------------------+----------
 public | clients | table | postgres=arwdDxt/postgres       +|                   | 
        |         |       | "test-simple-user"=arwd/postgres |                   | 
 public | orders  | table | postgres=arwdDxt/postgres       +|                   | 
        |         |       | "test-simple-user"=arwd/postgres |                   | 
(2 rows)

test_db=# 
```

#### Проверяем пермишны на таблицы в test_db:
```commandline
test_db=# \du
                                       List of roles
    Role name     |                         Attributes                         | Member of 
------------------+------------------------------------------------------------+-----------
 postgres         | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 test-admin-user  |                                                            | {}
 test-simple-user | Cannot login                                               | {}

test_db=# select * from information_schema.table_privileges WHERE grantee in ('test-simple-user','test-admin-user');
 grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 postgres | test-simple-user | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRIGGER        | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRIGGER        | NO           | NO
(22 rows)
```

#### Описание таблиц:
```commandline
test_db=# \d clients
               Table "public.clients"
  Column  |  Type   | Collation | Nullable | Default 
----------+---------+-----------+----------+---------
 id       | integer |           | not null | 
 lastname | text    |           |          | 
 country  | text    |           |          | 
 zakaz    | integer |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "country_idx" btree (country)
Foreign-key constraints:
    "clients_zakaz_fkey" FOREIGN KEY (zakaz) REFERENCES orders(id)

test_db=# \d orders
               Table "public.orders"
 Column |  Type   | Collation | Nullable | Default 
--------+---------+-----------+----------+---------
 id     | integer |           | not null | 
 name   | text    |           |          | 
 price  | integer |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_zakaz_fkey" FOREIGN KEY (zakaz) REFERENCES orders(id)

```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

#### Заполняем таблицы:
```commandline
test_db=# INSERT INTO orders VALUES (1, 'Шоколад', 10), (2, 'Принтер', 3000), (3, 'Книга', 500), (4, 'Монитор', 7000), (5, 'Гитара', 4000);
INSERT 0 5
test_db=# INSERT INTO clients VALUES (1, 'Иванов Иван Иванович', 'USA'), (2, 'Петров Петр Петрович', 'Canada'), (3, 'Иоганн Себастьян Бах', 'Japan'), (4, 'Ронни Джеймс Дио', 'Russia'), (5, 'Ritchie Blackmore', 'Russia');
INSERT 0 5
```

Проверка:
```commandline
test_db=# SELECT * FROM orders;
 id |  name   | price 
----+---------+-------
  1 | Шоколад |    10
  2 | Принтер |  3000
  3 | Книга   |   500
  4 | Монитор |  7000
  5 | Гитара  |  4000
(5 rows)

test_db=# SELECT * FROM clients;
 id |       lastname       | country | zakaz 
----+----------------------+---------+-------
  1 | Иванов Иван Иванович | USA     |      
  2 | Петров Петр Петрович | Canada  |      
  3 | Иоганн Себастьян Бах | Japan   |      
  4 | Ронни Джеймс Дио     | Russia  |      
  5 | Ritchie Blackmore    | Russia  |      
(5 rows)
```

#### Кол-во записей для каждой таблицы:
```commandline
test_db=# SELECT COUNT (*) FROM clients;
 count 
-------
     5
(1 row)

test_db=# SELECT COUNT (*) FROM orders;
 count 
-------
     5
(1 row)
```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказка - используйте директиву `UPDATE`.

#### Пользователи выполнили заказы:
```commandline
test_db=# UPDATE clients SET zakaz = 3 WHERE id = 1;
UPDATE 1
test_db=# UPDATE clients SET zakaz = 4 WHERE id = 2;
UPDATE 1
test_db=# UPDATE clients SET zakaz = 5 WHERE id = 3;
UPDATE 1
```

#### Все пользователи, совершившие заказ:
```commandline
test_db=# SELECT * FROM clients WHERE zakaz IS NOT NULL;
 id |       lastname       | country | zakaz 
----+----------------------+---------+-------
  1 | Иванов Иван Иванович | USA     |     3
  2 | Петров Петр Петрович | Canada  |     4
  3 | Иоганн Себастьян Бах | Japan   |     5
(3 rows)
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

#### Пример выполнения команды:
```commandline
test_db=# EXPLAIN SELECT * FROM clients WHERE zakaz IS NOT NULL;
                        QUERY PLAN                         
-----------------------------------------------------------
 Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72)
   Filter: (zakaz IS NOT NULL)
(2 rows)
```
Запрос показывает стоимость исполнения запроса, и фильтрацию по полю zakaz для выборки.

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

#### Создаём бэкап данных на vol_backup:
```commandline
dekar@Dekar-NIX:~$ docker exec -t postgres12 pg_dump -U postgres test_db -f /backup/dump_test_db.sql
dekar@Dekar-NIX:~$ sudo ls -la /var/lib/docker/volumes/vol_backup/_data
total 12
drwxr-xr-x 2 node_exporter sambashare 4096 фев 20 18:21 .
drwx-----x 3 root          root       4096 фев 20 14:08 ..
-rw-r--r-- 1 root          root       2677 фев 20 18:21 dump_test_db.sql
```

#### Поднимаем пустой контейнер с Postgres12:
```commandline
dekar@Dekar-NIX:~$ docker run --name postgres12_new -e POSTGRES_PASSWORD=Qwerty12345 --rm -d -p 5433:5432 -v vol_backup:/backup postgres:12
f1266bf862b324928333d7af991f79f872929e379f11085cd1a94be359b8b306
dekar@Dekar-NIX:~$ docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
f1266bf862b3   postgres:12   "docker-entrypoint.s…"   16 seconds ago   Up 16 seconds   0.0.0.0:5433->5432/tcp, :::5433->5432/tcp   postgres12_new
355c845fe0d1   postgres:12   "docker-entrypoint.s…"   2 hours ago      Up 2 hours      0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres12
```

#### Восстанавливаем базу на новом Postgres из бэкапа:
```commandline
dekar@Dekar-NIX:~$ docker exec -it postgres12_new psql -U postgres -c 'CREATE DATABASE test_db;'
CREATE DATABASE
dekar@Dekar-NIX:~$ docker exec -it postgres12_new psql -U postgres -d test_db -f /backup/dump_test_db.sql
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
COPY 5
COPY 5
ALTER TABLE
ALTER TABLE
CREATE INDEX
ALTER TABLE
psql:/backup/dump_test_db.sql:111: ERROR:  role "test-admin-user" does not exist
psql:/backup/dump_test_db.sql:118: ERROR:  role "test-simple-user" does not exist
psql:/backup/dump_test_db.sql:119: ERROR:  role "test-admin-user" does not exist
psql:/backup/dump_test_db.sql:126: ERROR:  role "test-simple-user" does not exist
psql:/backup/dump_test_db.sql:127: ERROR:  role "test-admin-user" does not exist
```
Как видим разрешения ролей не были предоставлены, т.к. их не существует на новом сервере postgres12.
Для бэкапа всех баз данных, включая информацию о ролях и табличных пространствах можно воспользоваться pg_dumpall.

#### Подключаемся к новому контейнеру и проверяем восстановленную базу данных:
```commandline
psql --host=127.0.0.1 --port=5433 --username=postgres
Password for user postgres: 
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 12.10 (Debian 12.10-1.pgdg110+1))
Type "help" for help.

postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)
postgres=# \c test_db
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 12.10 (Debian 12.10-1.pgdg110+1))
You are now connected to database "test_db" as user "postgres".
test_db=# SELECT * FROM clients;
 id |       lastname       | country | zakaz 
----+----------------------+---------+-------
  4 | Ронни Джеймс Дио     | Russia  |      
  5 | Ritchie Blackmore    | Russia  |      
  1 | Иванов Иван Иванович | USA     |     3
  2 | Петров Петр Петрович | Canada  |     4
  3 | Иоганн Себастьян Бах | Japan   |     5
(5 rows)

test_db=# SELECT * FROM orders;
 id |  name   | price 
----+---------+-------
  1 | Шоколад |    10
  2 | Принтер |  3000
  3 | Книга   |   500
  4 | Монитор |  7000
  5 | Гитара  |  4000
(5 rows)

test_db=# SELECT * FROM clients WHERE zakaz IS NOT NULL;
 id |       lastname       | country | zakaz 
----+----------------------+---------+-------
  1 | Иванов Иван Иванович | USA     |     3
  2 | Петров Петр Петрович | Canada  |     4
  3 | Иоганн Себастьян Бах | Japan   |     5
(3 rows)
```