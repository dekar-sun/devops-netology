# Курсовая работа по итогам модуля "DevOps и системное администрирование"

Курсовая работа необходима для проверки практических навыков, полученных в ходе прохождения курса "DevOps и системное администрирование".

Мы создадим и настроим виртуальное рабочее место. Позже вы сможете использовать эту систему для выполнения домашних заданий по курсу

## Задание

1. Создайте виртуальную машину Linux.
##### ВМ установлена:
```bash
[root@centos7 ~]# cat /etc/os-release 
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="https://www.centos.org/"
BUG_REPORT_URL="https://bugs.centos.org/"

CENTOS_MANTISBT_PROJECT="CentOS-7"
CENTOS_MANTISBT_PROJECT_VERSION="7"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="7"

[root@centos7 ~]# uname -a
Linux centos7 3.10.0-1160.49.1.el7.x86_64 #1 SMP Tue Nov 30 15:51:32 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

2. Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.
##### В качестве фаервола будем использовать фаервол из комплекта centos 7 - firewalld
Проверяем, что фаервол запущен:
```bash
[root@centos7 ~]# firewall-cmd --state
running
```
Проверяем активные зоны:
```bash
[root@centos7 ~]# firewall-cmd --get-zones
block dmz docker drop external home internal public trusted work
[root@centos7 ~]# firewall-cmd --get-active-zones
docker
  interfaces: docker0
public
  interfaces: enp0s3
[root@centos7 ~]# 
```
Проверяем правила для зоны public:
```bash
[root@centos7 ~]#  firewall-cmd --zone=public --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources: 
  services: ssh
  ports: 
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```
Добавляем сервис https к зоне public:
```bash
[root@centos7 ~]# firewall-cmd --zone=public --permanent --add-service=https
success
[root@centos7 ~]# firewall-cmd --reload
success
[root@centos7 ~]# firewall-cmd --zone=public --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources: 
  services: https ssh
  ports: 
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```
Дабы убедиться, что 443 порт разрешён смотрим на содержимое файла сервиса:
```bash
[root@centos7 ~]# more /usr/lib/firewalld/services/https.xml 
<?xml version="1.0" encoding="utf-8"?>
<service>
  <short>Secure WWW (HTTPS)</short>
  <description>HTTPS is a modified HTTP used to serve Web pages when security is important. Examples are sites that require logins like stores or web mail. This option
 is not required for viewing pages locally or developing Web pages. You need the httpd package installed for this option to be useful.</description>
  <port protocol="tcp" port="443"/>
</service>
```
Добавляем lo интерфейс в доверенную зону:
```bash
[root@centos7 ~]# firewall-cmd --permanent --zone=trusted --add-interface=lo
success
```

3. Установите hashicorp vault ([инструкция по ссылке](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started#install-vault)).
##### Vault установлен:
```bash
[root@centos7 ~]# vault --version
Vault v1.9.2 (f4c6d873e2767c0d6853b5d9ffc77b0d297bfbdf)
```

4. Cоздайте центр сертификации по инструкции ([ссылка](https://learn.hashicorp.com/tutorials/vault/pki-engine?in=vault/secrets-management)) и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).
##### Запускаем vault в dev режиме:
```bash
[root@centos7 ~]# vault server -dev -dev-root-token-id root
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.17.5
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.9.2
             Version Sha: f4c6d873e2767c0d6853b5d9ffc77b0d297bfbdf
```
Добавляем переменные в окружение:
```bash
[root@centos7 ~]# export VAULT_ADDR=http://127.0.0.1:8200
[root@centos7 ~]# export VAULT_TOKEN=root
[root@centos7 ~]# env | grep -i vault
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=root
```
Генерируем корневой сертификат для СА:
```bash
[root@centos7 ~]# vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
[root@centos7 ~]# vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
[root@centos7 ~]# vault write -field=certificate pki/root/generate/internal \
>      common_name="example.com" \
>      ttl=87600h > CA_cert.crt
```
Генерируем промежуточный сертификат:
```bash
[root@centos7 ~]# vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
[root@centos7 ~]# vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
[root@centos7 ~]# vault write -format=json pki_int/intermediate/generate/internal \
>      common_name="example.com Intermediate Authority" \
>      | jq -r '.data.csr' > pki_intermediate.csr
```

Подписываем промежуточный сертификат корневым сертификатом нашего СА:
```bash
[root@centos7 ~]# vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
>      format=pem_bundle ttl="43800h" \
>      | jq -r '.data.certificate' > intermediate.cert.pem
[root@centos7 ~]# vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
```

Итого полученные файлы:
```bash
[root@centos7 ~]# ll
total 12
-rw-r--r--. 1 root root 1171 янв 18 15:45 CA_cert.crt
-rw-r--r--. 1 root root 1172 янв 18 16:02 intermediate.cert.pem
-rw-r--r--. 1 root root  924 янв 18 16:01 pki_intermediate.csr
```
Добавим vault роль для нашего сайта:
```bash
vault write pki_int/roles/example-dot-com \
     allowed_domains="example.com" \
     allow_subdomains=true \
     max_ttl="720h"
```
Генерируем сертификат для сайта:
```bash
[root@centos7 ~]# vault write -format=json pki_int/issue/example-dot-com common_name="diplom.example.com" ttl="720h" > diplom.crt
```

Разделяем diplom.crt на составляющие для nginx и скопируем в каталог /etc/ssl: 
```bash
[root@centos7 ~]# cat diplom.crt | jq -r .data.certificate > /etc/ssl/diplom.pem
[root@centos7 ~]# cat diplom.crt | jq -r .data.ca_chain[] >> /etc/ssl/diplom.pem
[root@centos7 ~]# cat diplom.crt | jq -r .data.private_key > /etc/ssl/diplom.key
```

5. Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.
Сертификат установлен. Скриншот свойств корневого сертификата в браузере на скриншоте Screenshot_CA_Installed_in_browser.png

6. Установите nginx.
nginx установлен:
```bash
[root@centos7 ~]# nginx -v
nginx version: nginx/1.20.1
```

7. По инструкции ([ссылка](https://nginx.org/en/docs/http/configuring_https_servers.html)) настройте nginx на https, используя ранее подготовленный сертификат:
  - можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
  - можно использовать и другой html файл, сделанный вами;
Создадим для нашего сайта конфигурационный файл в /etc/nginx/sites-available/ со следующим содержанием:
```bash
[root@centos7 ~]# cat /etc/nginx/sites-available/diplom.conf
server {
        listen       443 ssl;
        listen       [::]:443 ssl;
        server_name  diplom.example.com;
        root         /usr/share/nginx/html;

        ssl_certificate "/etc/ssl/diplom.pem";
        ssl_certificate_key "/etc/ssl/diplom.key";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout 10m;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        error_page 404 /404.html;
            location = /40x.html {
        }
        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
      }
```
Создадим символьную ссылку на наш конфиг и перечитаем настройки nginx:
```bash
[root@centos7 ~]# ln -s /etc/nginx/sites-available/diplom.conf /etc/nginx/sites-enabled/
[root@centos7 ~]# systemctl reload nginx
```

8. Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.
Скриншот открытого сайта представлен в файле Screenshot_Site_Opened_in_browser.png.
Как можно видеть, браузер доверяет сертификату сайта.

9. Создайте скрипт, который будет генерировать новый сертификат в vault:
  - генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
  - перезапускаем nginx для применения нового сертификата.
Скрипт для генерации нового сертификата, при условии запущенного vault:
```bash
  #!/usr/bin/env bash

  dplm="/root/diplom.crt"
  #get old certificate date
  old_date=$(stat -c '%z' "$dplm")

  #create certificate, 30 days
  vault write -format=json pki_int/issue/example-dot-com common_name="diplom.example.com" ttl="720h" > "$dplm"

  new_date=$(stat -c '%z' "$dplm")/

  if [[ "$new_date" > "$old_date" ]]; then
        #create separate certificates for nginx config
        diplom=$(cat $dplm)        
        echo $diplom | jq -r .data.certificate > /etc/ssl/diplom.pem
        echo $diplom | jq -r .data.ca_chain[] >> /etc/ssl/diplom.pem
        echo $diplom | jq -r .data.private_key > /etc/ssl/diplom.key
        systemctl reload nginx.service

  else
        exit
  fi
```

10. Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.

Добавляем содержимое скрипта из задания 9 в файл renew_crt.sh, выдаём ему права на исполнение и запускаем crontab -e для добавления задания.
Итоговое задание для cron:
```bash
[root@centos7 ~]# crontab -l
0 0 30 * * /root/renew_crt.sh
```

11. В современных системах, имеющих систему инициализации systemd, более современным методом для создания периодической задачи, на мой взгляд, будет использование таймеров systemd.
В этом случае вначале необходимо создать systemd unit для скрипта:
```editorconfig
[root@centos7 ~]# cat /etc/systemd/system/renew_crt.service
[Unit]
Description=Cert Renew Service
Wants=nginx.service
[Service]
Type=oneshot
User=root
Group=root
Environment="VAULT_ADDR=http://127.0.0.1:8200" "VAULT_TOKEN=root" "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root"
ExecStart=/root/renew_crt.sh
[Install]
WantedBy=multi-user.target
```
Проверяем:
```commandline
[root@centos7 ~]# systemctl daemon-reload
[root@centos7 ~]# systemctl start renew_crt.service
[root@centos7 ~]# systemctl status renew_crt.service -l
● renew_crt.service - Cert Renew Service
   Loaded: loaded (/etc/systemd/system/renew_crt.service; disabled; vendor preset: disabled)
   Active: inactive (dead)

янв 18 23:15:29 centos7 systemd[1]: Starting Cert Renew Service...
янв 18 23:15:29 centos7 systemd[1]: Started Cert Renew Service.
```

Видим, что сервис успешно стартует. При этом сертификаты выпускаются (судя по дате):
```commandline
[root@centos7 ~]# ls -la diplom.crt 
-rw-r--r--. 1 root root 5753 янв 18 23:15 diplom.crt
[root@centos7 ~]# ls -la /etc/ssl | grep diplom
-rw-r--r--.  1 root root 1679 янв 18 23:15 diplom.key
-rw-r--r--.  1 root root 2417 янв 18 23:15 diplom.pem
```

Создадим таймер:

```commandline
[root@centos7 ~]# cat /etc/systemd/system/renew_crt.timer
[Unit]
Description=Cert Renew Service Timer
[Timer]
OnCalendar=*-*-30 00:00
[Install]
WantedBy=timers.target
```

Запустим таймер:
```commandline
[root@centos7 ~]# systemctl status renew_crt.timer
● renew_crt.timer - Cert Renew Service Timer
   Loaded: loaded (/etc/systemd/system/renew_crt.timer; disabled; vendor preset: disabled)
   Active: active (waiting) since Вт 2022-01-18 23:20:56 MSK; 2s ago
  Trigger: Sun 2022-01-30 00:00:00 MSK; 1 weeks 4 days left
 Triggers: ● renew_crt.service

янв 18 23:55:56 centos7 systemd[1]: Started Cert Renew Service Timer.
```
Видно, что следующий запуск запланирован на 30 января на 00:00. При этом все логи выполнения скрипта доступны через journalctl -u renew_crt.service.