# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
   ```
   { "info" : "Sample JSON output from our service\t",
       "elements" :[
           { "name" : "first",
           "type" : "server",
           "ip" : 7175 
           },
           { "name" : "second",
           "type" : "proxy",
           "ip : 71.78.22.43
           }
       ]
   }
   ```

Нужно найти и исправить все ошибки, которые допускает наш сервис.
В Json, возвращаемом сервисом отсутствуют кавычки у строки номер 9 с ip адресом.
Исправленный json:

 ```json lines
1. { "info" : "Sample JSON output from our service\t",
2.       "elements" :[
3.           { "name" : "first",
4.           "type" : "server",
5.           "ip" : 7175 
6.           },
7.           { "name" : "second",
8.           "type" : "proxy",
9.           "ip" : "71.78.22.43"
10.           }
11.       ]
12. }
```

2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному
   функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по
   одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в
   момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

Готовый скрипт:

```python
#!/usr/bin/env python3
import socket
from time import sleep
import datetime
import json
import yaml

wait = 5  # pause between verifications in seconds

hosts = {'drive.google.com': '1.1.1.1', 'mail.google.com': '1.1.1.1', 'google.com': '1.1.1.1'}

services_error_pool = []

while True:

    for x in hosts:
        ip = socket.gethostbyname(x)
        if ip != hosts[x]:
            print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + ' [ERROR] ' + str(x) + ' IP mismatch: ' +
                  hosts[x] + ' ' + ip)
            hosts[x] = ip
            # json
            with open('./' + x + '.json', 'w') as json_file:
                json_data = json.dumps({x: ip})
                json_file.write(json_data)
            # yaml
            with open('./' + x + '.yml', 'w') as yml_file:
                yml_data = yaml.dump([{x: ip}])
                yml_file.write(yml_data)
            # Create one file for all services in Json and yaml
            services_error_pool.append({x: ip})
            with open('./' + 'services.json', 'w') as json_file:
                json_data = json.dumps(services_error_pool)
                json_file.write(json_data)
            with open('./' + 'services.yml', 'w') as yml_file:
                yml_data = yaml.dump(services_error_pool)
                yml_file.write(yml_data)
        else:
            print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + ' ' + str(x) + ' ' + ip)
    sleep(wait)
    print('-----------------------------------------------------------------------------------------------------------')

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных
использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:

* Принимать на вход имя файла
* Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
* Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
* Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
* При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
* Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

Предлагаю к рассмотрению нижеприведённый вариант скрипта для перевода из JSON в YAML, и из YAML в JSON.
В нём пока не реализована валидация ошибок - нехватило времени :(

```python
#!/usr/bin/env python3

import sys
import json
import yaml

if len(sys.argv) > 1:
    file = sys.argv[1]
    with open('./' + file, 'r') as j_file:
        try:
            json_file = json.load(j_file)
            with open('./' + file.split('.')[0] + '.yml', 'w') as yml_file:
                yml_data = yaml.dump(json_file)
                yml_file.write(yml_data)
        except Exception:
            try:
                with open('./' + file, 'r') as y_file:
                    yaml_file = yaml.safe_load(y_file)
                    print(yaml_file)
                with open('./' + file.split('.')[0] + '.json', 'w') as jsn_file:
                    jsn_data = json.dumps(yaml_file)
                    jsn_file.write(jsn_data)
            except Exception:
                print('This is not json or yaml file')
```