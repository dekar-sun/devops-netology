# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

#### Скачиваем PostgreSQL 13ой версии и создаём volumes:
```commandline
dekar@Dekar-NIX:~$ docker pull postgres:13
13: Pulling from library/postgres
5eb5b503b376: Already exists 
daa0467a6c48: Already exists 
7cf625de49ef: Already exists 
bb8afcc973b2: Already exists 
c74bf40d29ee: Already exists 
2ceaf201bb22: Already exists 
1255f255c0eb: Already exists 
12a9879c7aa1: Already exists 
0052b4855bef: Pull complete 
e1392be26b85: Pull complete 
9154b308134e: Pull complete 
7e0447003684: Pull complete 
3d7ffb6e96a5: Pull complete 
Digest: sha256:8b8ff4fcdc9442d8a1d38bd1a77acbdfbc8a04afda9c19df47383cb2d08fc04b
Status: Downloaded newer image for postgres:13
docker.io/library/postgres:13
dekar@Dekar-NIX:~$ docker volume create vol_pg
vol_pg
dekar@Dekar-NIX:~$ docker volume create vol_backup
vol_backup
```

####  Запускаем контейнер:
```commandline
dekar@Dekar-NIX:~$ docker run --name postgres13 -e POSTGRES_PASSWORD=Qwerty12345 --rm -d -p 5432:5432 -v vol_pg:/var/lib/postgresql/data -v vol_backup:/backup postgres:13
69b3a1e3b1c272d32f172a86f6e3d296352109bc0b24c4139593c2bc2f4e7d4f
dekar@Dekar-NIX:~$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS        PORTS                                       NAMES
69b3a1e3b1c2   postgres:13   "docker-entrypoint.s…"   3 seconds ago   Up 1 second   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres13
```

#### Подключаемся к базе:
```commandline
dekar@Dekar-NIX:~$ psql --host=127.0.0.1 --port=5432 --username=postgres
Password for user postgres: 
psql (13.6 (Ubuntu 13.6-1.pgdg20.04+1))
Type "help" for help.

```

#### Выводим список БД:
```commandline
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```

#### Пробуем подключиться к БД template1:
```commandline
postgres=# \c template1
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 13.6 (Debian 13.6-1.pgdg110+1))
WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
You are now connected to database "template1" as user "postgres".
```

#### Выводим список таблиц базы:
```commandline
template1=# \dt
Did not find any relations.
```
Как видим в данной базе отсутствуют таблицы. Можно воспользоваться командой `dtS` для просмотра системных таблиц.
```commandline
                    List of relations
   Schema   |          Name           | Type  |  Owner   
------------+-------------------------+-------+----------
 pg_catalog | pg_aggregate            | table | postgres
 pg_catalog | pg_am                   | table | postgres
 pg_catalog | pg_amop                 | table | postgres
 pg_catalog | pg_amproc               | table | postgres
 pg_catalog | pg_attrdef              | table | postgres
 pg_catalog | pg_attribute            | table | postgres
 pg_catalog | pg_auth_members         | table | postgres
 pg_catalog | pg_authid               | table | postgres
 pg_catalog | pg_cast                 | table | postgres
 pg_catalog | pg_class                | table | postgres
 pg_catalog | pg_collation            | table | postgres
 pg_catalog | pg_constraint           | table | postgres
 pg_catalog | pg_conversion           | table | postgres
 pg_catalog | pg_database             | table | postgres
 pg_catalog | pg_db_role_setting      | table | postgres
 pg_catalog | pg_default_acl          | table | postgres
 pg_catalog | pg_depend               | table | postgres
 pg_catalog | pg_description          | table | postgres
 pg_catalog | pg_enum                 | table | postgres
 pg_catalog | pg_event_trigger        | table | postgres
 pg_catalog | pg_extension            | table | postgres
 pg_catalog | pg_foreign_data_wrapper | table | postgres
 pg_catalog | pg_foreign_server       | table | postgres
 pg_catalog | pg_foreign_table        | table | postgres
 pg_catalog | pg_index                | table | postgres
 pg_catalog | pg_inherits             | table | postgres
 pg_catalog | pg_init_privs           | table | postgres
 pg_catalog | pg_language             | table | postgres
 ...
```

#### Посмотрим содержимое таблицы pg_aggregate:
```commandline
postgres=# \d pg_aggregate
               Table "pg_catalog.pg_aggregate"
      Column      |   Type   | Collation | Nullable | Default 
------------------+----------+-----------+----------+---------
 aggfnoid         | regproc  |           | not null | 
 aggkind          | "char"   |           | not null | 
 aggnumdirectargs | smallint |           | not null | 
 aggtransfn       | regproc  |           | not null | 
 aggfinalfn       | regproc  |           | not null | 
 aggcombinefn     | regproc  |           | not null | 
 aggserialfn      | regproc  |           | not null | 
 aggdeserialfn    | regproc  |           | not null | 
 aggmtransfn      | regproc  |           | not null | 
 aggminvtransfn   | regproc  |           | not null | 
 aggmfinalfn      | regproc  |           | not null | 
 aggfinalextra    | boolean  |           | not null | 
 aggmfinalextra   | boolean  |           | not null | 
 aggfinalmodify   | "char"   |           | not null | 
 aggmfinalmodify  | "char"   |           | not null | 
 aggsortop        | oid      |           | not null | 
 aggtranstype     | oid      |           | not null | 
 aggtransspace    | integer  |           | not null | 
 aggmtranstype    | oid      |           | not null | 
 aggmtransspace   | integer  |           | not null | 
 agginitval       | text     | C         |          | 
 aggminitval      | text     | C         |          | 
Indexes:
    "pg_aggregate_fnoid_index" UNIQUE, btree (aggfnoid)
```

#### Выходим из psql:
```commandline
postgres=# \q
dekar@Dekar-NIX:~$ 
```

## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

#### Подключаемся обратно к postgres13 и создаём ДБ `test_database`
```commandline
dekar@Dekar-NIX:~$ psql --host=127.0.0.1 --port=5432 --username=postgres
Password for user postgres: 
psql (13.6 (Ubuntu 13.6-1.pgdg20.04+1))
Type "help" for help.


postgres=# CREATE DATABASE test_database;
CREATE DATABASE
postgres=# \l
                                   List of databases
     Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
---------------+----------+----------+------------+------------+-----------------------
 postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)
```

#### Восстанавливаем ДБ test_database из приложенного к заданию бэкапа в соседнем окне терминала. При этом сам бэкап был скопирован в volume vol_backup: `/var/lib/docker/volumes/vol_backup/_data`.
```commandline
dekar@Dekar-NIX:~$ docker exec -it postgres13 psql -U postgres -d test_database -f /backup/test_dump.sql
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
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE
```

#### Подключаемся к базе test_database и смотрим на таблицы восстановленой БД:
```commandline
postgres=# \c test_database
You are now connected to database "test_database" as user "postgres".
test_database=# 
test_database=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```

#### Находим столбец таблицы `orders` с наибольшим средним значением размера элементов в байтах:
```commandline
test_database=# SELECT avg_width, attname FROM pg_stats WHERE TABLENAME='orders';
 avg_width | attname 
-----------+---------
         4 | id
        16 | title
         4 | price
(3 rows)
```
Видим что такой столбец это `title`.

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?


#### Так как преобразовать обычную таблицу в секционированную и наоборот нельзя, переименуем существующую таблицу `orders`, создадим новую с указанием секционирования:
```commandline
test_database=# ALTER TABLE orders RENAME TO orders_old;
ALTER TABLE
test_database=# CREATE TABLE orders (id integer, title varchar(80), price integer) PARTITION BY RANGE(price);
CREATE TABLE
test_database=# \dt
                 List of relations
 Schema |    Name    |       Type        |  Owner   
--------+------------+-------------------+----------
 public | orders     | partitioned table | postgres
 public | orders_old | table             | postgres
(2 rows)
```

#### Создаём таблицы orders_1 - price>499 и orders_2 - price<=499: 
```commandline
test_database=# CREATE TABLE orders_1 PARTITION OF orders FOR VALUES FROM (500) TO (MAXVALUE);
CREATE TABLE
test_database=# CREATE TABLE orders_2 PARTITION OF orders FOR VALUES FROM (MINVALUE) TO (500);
CREATE TABLE
test_database=# \dt
                 List of relations
 Schema |    Name    |       Type        |  Owner   
--------+------------+-------------------+----------
 public | orders     | partitioned table | postgres
 public | orders_1   | table             | postgres
 public | orders_2   | table             | postgres
 public | orders_old | table             | postgres
(4 rows)
```

#### Заполняем созданную partitioned таблицу orders и проверяем значения в `orders_1` и `orders_2`:
```commandline
test_database=# INSERT INTO orders (id, title, price) SELECT * FROM orders_old;
INSERT 0 8
test_database=# SELECT * FROM orders_1;
 id |       title        | price 
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)

test_database=# SELECT * FROM orders_2;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)
```
Ручное разбиение таблицы orders можно было исключить, если бы изначально, при проектировании создали бы её как секционированную.

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

#### Создаём бэкап базы `test_database`:
```commandline
dekar@Dekar-NIX:~$ docker exec -t postgres13 pg_dump -U postgres test_database -f /backup/dump_test_database.sql
dekar@Dekar-NIX:~$ sudo ls -la /var/lib/docker/volumes/vol_backup/_data
total 16
drwxr-xr-x 2 node_exporter sambashare 4096 фев 26 15:25 .
drwx-----x 3 root          root       4096 фев 20 14:08 ..
-rw-r--r-- 1 root          root       3473 фев 26 15:25 dump_test_database.sql
-rw-r--r-- 1 root          root       2082 фев 26 13:42 test_dump.sql
```

Для добавления уникальности столбца `title` можно создать индекс по столбцу:
```commandline
CREATE UNIQUE INDEX title_idx ON public.orders (title);
```
---
