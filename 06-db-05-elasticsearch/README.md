# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.


#### Docker manifest представлен в [Dockerfile](elk/Dockerfile):
Образ запускался на macos с arm процессорром, поэтому архитектура elasticsearch была выбрана aarch64.
Настройки elasticsearch представлены в файле [elasticsearch.yml](elk/elasticsearch.yml).
Образ удалось загрузить на docker hub. Он доступен по [ссылке](https://hub.docker.com/layers/klauswoof/elasticsearch/7.17.1/images/sha256-8460b6776a69ad6faa5ee27cbceab0f39b9d86e29aeefe0f909b131e42df87e6?context=explore).

Для запуска контейнера был составлен docker-compose file: [docker-compose.yml](elk/docker-compose.yml)
Запускаем контейнер и проверяем elasticsearch:
```commandline
[17:31:37] [~] ❱❱❱ docker-compose up -d
[+] Running 1/1
 ⠿ Container elasticsearch  Started                                                                                                                                                                            0.5s
[17:31:39] [cost 0.983s] docker-compose up -d
[16:58:28] [~] ❱❱❱ curl -X GET localhost:9200
{
  "name" : "0b240395ea63",
  "cluster_name" : "netology_test",
  "cluster_uuid" : "lbBn8ODLREiSdHgdLYizCQ",
  "version" : {
    "number" : "7.17.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "e5acb99f822233d62d6444ce45a4543dc1c8059a",
    "build_date" : "2022-02-23T22:20:54.153567231Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
[16:58:31] [cost 0.208s] curl -X GET localhost:9200
```

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

#### Создаём индексы:
```commandline
[17:03:46] [~] ❱❱❱ curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}%                                                                                                                                                   [17:03:48] [cost 0.356s] curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'

[17:03:58] [~] ❱❱❱ curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}%                                                                                                                                                   [17:03:59] [cost 0.273s] curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'

[17:04:16] [~] ❱❱❱ curl -X PUT localhost:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}%                                                                                                                                                   [17:04:18] [cost 0.259s] curl -X PUT localhost:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'

[17:04:21] [~] ❱❱❱
```

#### Список индексов:
```commandline
[17:06:06] [~] ❱❱❱ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases LK6lRjwtT8a8KMZHQK0faA   1   0         45            0     42.5mb         42.5mb
green  open   ind-1            xweKrxbuTZaCa9f5i3pt1A   1   0          0            0       226b           226b
yellow open   ind-3            VORWIUNlSVy8jlqdMNIfEQ   4   2          0            0       904b           904b
yellow open   ind-2            7PDi54xFSI-buRWosf3ngw   2   1          0            0       452b           452b
[17:06:07] [cost 0.212s] curl -X GET 'http://localhost:9200/_cat/indices?v'
```

#### Cтатус индексов:
```commandline
[17:07:03] [~] ❱❱❱ curl -X GET 'http://localhost:9200/_cluster/health/ind-1?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

[17:07:48] [~] ❱❱❱ curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 2,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 2,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
[17:07:53] [cost 0.231s] curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'

[17:07:53] [~] ❱❱❱ curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 8,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
[17:07:57] [cost 0.103s] curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'
```

#### Статус кластера:
```commandline
[17:09:13] [~] ❱❱❱ curl -XGET 'http://localhost:9200/_cluster/health/?pretty=true'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```
У индексов ind-2 и ind-3 указано кол-во реплик. Но т.к. других серверов elasticsearch в кластере нет - поэтому у данных индексов статус yellow.
По этой же причине у всего кластера такой же статус.

#### Удаляем индексы:
```commandline
[17:14:47] [~] ❱❱❱ curl -X DELETE 'http://localhost:9200/ind-1?pretty'
{
  "acknowledged" : true
}
[17:14:50] [cost 0.211s] curl -X DELETE 'http://localhost:9200/ind-1?pretty'

[17:14:51] [~] ❱❱❱ curl -X DELETE 'http://localhost:9200/ind-2?pretty'
{
  "acknowledged" : true
}
[17:14:55] [cost 0.169s] curl -X DELETE 'http://localhost:9200/ind-2?pretty'

[17:14:55] [~] ❱❱❱ curl -X DELETE 'http://localhost:9200/ind-3?pretty'
{
  "acknowledged" : true
}
[17:14:58] [cost 0.215s] curl -X DELETE 'http://localhost:9200/ind-3?pretty'

[17:14:58] [~] ❱❱❱ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases LK6lRjwtT8a8KMZHQK0faA   1   0         45            0     42.5mb         42.5mb
[17:15:04] [cost 0.137s] curl -X GET 'http://localhost:9200/_cat/indices?v'
```

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

---

#### Создаём snapshot repository:
```commandline
[18:02:37] [~] ❱❱❱ curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d' { "type": "fs", "settings": { "location": "/elasticsearch-7.17.1/snapshots" } }'
{
  "acknowledged" : true
}
```

Проверяем:
```commandline
[18:04:49] [~] ❱❱❱ curl -X POST "localhost:9200/_snapshot/netology_backup/_verify?pretty"
{
  "nodes" : {
    "TsY9ydLbTvC_aHyU3EFkCQ" : {
      "name" : "27e928c6486f"
    }
  }
}
[18:09:39] [~] ❱❱❱ curl -X GET "localhost:9200/_snapshot/netology_backup?pretty"
{
  "netology_backup" : {
    "type" : "fs",
    "settings" : {
      "location" : "/elasticsearch-7.17.1/snapshots"
    }
  }
}
```

#### Создаём индекс test:
```commandline
[18:11:47] [~] ❱❱❱ curl -X PUT "localhost:9200/test" -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"test"}%
```

#### Список индексов:
```commandline
[18:13:43] [~] ❱❱❱ curl -X GET "localhost:9200/_cat/indices?v"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases hFsk7yNzS5uZ7Hvac1itZQ   1   0         45            0     42.5mb         42.5mb
green  open   test             UBTfD9OyShigrRmo6_b35Q   1   0          0            0       226b           226b
```

#### Создадим снэпшот:
```commandline
[18:15:54] [~] ❱❱❱ curl -X PUT "localhost:9200/_snapshot/netology_backup/elasticsearch?wait_for_completion=true"
{"snapshot":{"snapshot":"elasticsearch","uuid":"-WKdcnfATzSbCImIEWG-5g","repository":"netology_backup","version_id":7170199,"version":"7.17.1","indices":["test",".ds-.logs-deprecation.elasticsearch-default-2022.03.12-000001",".ds-ilm-history-5-2022.03.12-000001",".geoip_databases"],"data_streams":["ilm-history-5",".logs-deprecation.elasticsearch-default"],"include_global_state":true,"state":"SUCCESS","start_time":"2022-03-12T15:15:56.124Z","start_time_in_millis":1647098156124,"end_time":"2022-03-12T15:15:57.332Z","end_time_in_millis":1647098157332,"duration_in_millis":1208,"failures":[],"shards":{"total":4,"failed":0,"successful":4},"feature_states":[{"feature_name":"geoip","indices":[".geoip_databases"]}]}}%
```

#### Список файлов в каталоге snapshot:
```commandline
[18:16:56] [~] ❱❱❱ docker exec -it elasticsearch bash
[elasticsearch@27e928c6486f /]$ ll elasticsearch-7.17.1/snapshots/
total 48
-rw-r--r-- 1 elasticsearch elasticsearch  1425 Mar 12 15:15 index-0
-rw-r--r-- 1 elasticsearch elasticsearch     8 Mar 12 15:15 index.latest
drwxr-xr-x 6 elasticsearch elasticsearch  4096 Mar 12 15:15 indices
-rw-r--r-- 1 elasticsearch elasticsearch 29228 Mar 12 15:15 meta--WKdcnfATzSbCImIEWG-5g.dat
-rw-r--r-- 1 elasticsearch elasticsearch   712 Mar 12 15:15 snap--WKdcnfATzSbCImIEWG-5g.dat
```

#### Удаляем индекс test и создаём test-2:
```commandline
[18:19:45] [~] ❱❱❱ curl -X DELETE "localhost:9200/test?pretty"
{
  "acknowledged" : true
}
[18:22:42] [~] ❱❱❱ curl -X PUT "localhost:9200/test-2" -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"test-2"}%
```

#### Список индексов
```commandline
[18:23:25] [~] ❱❱❱ curl -X GET "localhost:9200/_cat/indices?v"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2           o4WzTtLnT86lATnUNwap6A   1   0          0            0       226b           226b
green  open   .geoip_databases hFsk7yNzS5uZ7Hvac1itZQ   1   0         45            0     42.5mb         42.5mb
```

#### Удаляем существующие data streams из кластера и восстанавливаем из бэкапа:
```commandline
[18:41:06] [~] ❱❱❱ curl -X DELETE "localhost:9200/_data_stream/*?expand_wildcards=all&pretty"
{
  "acknowledged" : true
}

[18:41:09] [~] ❱❱❱ curl -X POST "localhost:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty" -H 'Content-Type: application/json' -d' { "indices": "*", "include_global_state": true }'
{
  "accepted" : true
}
```

#### Выводим список индексов:
```commandline
[18:45:02] [~] ❱❱❱ curl -X GET "localhost:9200/_cat/indices?v"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2           o4WzTtLnT86lATnUNwap6A   1   0          0            0       226b           226b
green  open   .geoip_databases YWcUX7cTQauFe5SvXAh67w   1   0         45            0     42.5mb         42.5mb
green  open   test             uN6LXK_HQgahBVMJB1qlWw   1   0          0            0       226b           226b
```
