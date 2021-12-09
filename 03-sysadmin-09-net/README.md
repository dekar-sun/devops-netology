1. Bitwarden плагин успешно установлен, регистрация в системе пройдена. Получилось добавить записи связки логин\пароль и применить их
при входе на сайты.
2. Установлен Google authenticator на мобильный телефон. Настроен вход в Bitwarden аккаунт с помощью Google authenticator.

3. После установки apache2 и активации ssl плагина создаём самоподписанный сертификат и настраиваем конфиг apache:

```shell
udo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
> -keyout /etc/ssl/private/apache-selfsigned.key \
> -out /etc/ssl/certs/apache-selfsigned.crt \
> -subj "/C=RU/ST=Moscow/L=Moscow/O=Company Name/OU=Org/CN=www.example.com"
Generating a RSA private key
.....+++++
.....+++++
writing new private key to '/etc/ssl/private/apache-selfsigned.key'
-----
vagrant@vagrant:~/testssl.sh$ sudo vim /etc/apache2/sites-available/firmavenikov.conf
vagrant@vagrant:~/testssl.sh$ sudo mkdir /var/www/FirmaVenikov
vagrant@vagrant:~/testssl.sh$ sudo vim /var/www/FirmaVenikov/index.html
vagrant@vagrant:~/testssl.sh$ sudo a2ensite firmavenikov
Enabling site firmavenikov.
To activate the new configuration, you need to run:
  systemctl reload apache2
vagrant@vagrant:~/testssl.sh$ sudo apache2ctl configtest
Syntax OK
vagrant@vagrant:~/testssl.sh$ systemctl reload apache2
==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-units ===
Authentication is required to reload 'apache2.service'.
Authenticating as: vagrant,,, (vagrant)
Password: 
==== AUTHENTICATION COMPLETE ===
```
Запущенный сайт на хостовой машине с проброшенным портом 8443 представлен на скриншоте apache2.png.

4. Клонируем репозиторий testssl:
```shell
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
```
Задаем права запуска на файл testssl.sh:

```shell
vagrant@vagrant:~/testssl.sh$ chmod +x ./testssl.sh
```

Проверяем произвольный сайт на уязвимости:


<details>
<summary>Раскрыть</summary>

```shell
./testssl.sh -U --sneaky https://www.cisco.com

###########################################################
    testssl.sh       3.1dev from https://testssl.sh/dev/
    (2dce751 2021-12-09 17:03:57 -- )

      This program is free software. Distribution and
             modification under GPLv2 permitted.
      USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

       Please file bugs @ https://testssl.sh/bugs/

###########################################################

 Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
 on vagrant:./bin/openssl.Linux.x86_64
 (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")


 Start 2021-12-09 19:21:47        -->> 2.23.130.48:443 (www.cisco.com) <<--

 Further IP addresses:   2001:2030:21:1b1::b33 2001:2030:21:1ae::b33 
 rDNS (2.23.130.48):     a2-23-130-48.deploy.static.akamaitechnologies.com.
 Service detected:       HTTP


 Testing vulnerabilities 

 Heartbleed (CVE-2014-0160)                not vulnerable (OK), no heartbeat extension
 CCS (CVE-2014-0224)                       not vulnerable (OK)
 Ticketbleed (CVE-2016-9244), experiment.  not vulnerable (OK)
 ROBOT                                     Server does not support any cipher suites that use RSA key transport
 Secure Renegotiation (RFC 5746)           supported (OK)
 Secure Client-Initiated Renegotiation     VULNERABLE (NOT ok), DoS threat (6 attempts)
 CRIME, TLS (CVE-2012-4929)                not vulnerable (OK)
 BREACH (CVE-2013-3587)                    potentially NOT ok, "gzip" HTTP compression detected. - only supplied "/" tested
                                           Can be ignored for static pages or if no secrets in the page
 POODLE, SSL (CVE-2014-3566)               not vulnerable (OK)
 TLS_FALLBACK_SCSV (RFC 7507)              No fallback possible (OK), no protocol below TLS 1.2 offered
 SWEET32 (CVE-2016-2183, CVE-2016-6329)    not vulnerable (OK)
 FREAK (CVE-2015-0204)                     not vulnerable (OK)
 DROWN (CVE-2016-0800, CVE-2016-0703)      not vulnerable on this host and port (OK)
                                           make sure you don't use this certificate elsewhere with SSLv2 enabled services
                                           https://censys.io/ipv4?q=B26A300351FE254C585211A21050A5B194FD3DE7E5BBBDC700885062437E9BFF could help you to find out
 LOGJAM (CVE-2015-4000), experimental      not vulnerable (OK): no DH EXPORT ciphers, no DH key detected with <= TLS 1.2
 BEAST (CVE-2011-3389)                     not vulnerable (OK), no SSL3 or TLS1
 LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
 Winshock (CVE-2014-6321), experimental    not vulnerable (OK)
 RC4 (CVE-2013-2566, CVE-2015-2808)        no RC4 ciphers detected (OK)


 Done 2021-12-09 19:22:13 [  30s] -->> 2.23.130.48:443 (www.cisco.com) <<--
```
</details>


5. Проверяем установлен ли на виртуальной машине vagrant ssh сервер:
```shell
root@vagrant:~# systemctl status sshd
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-11-24 17:45:18 UTC; 2 weeks 0 days ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 689 (sshd)
      Tasks: 1 (limit: 2279)
     Memory: 6.7M
     CGroup: /system.slice/ssh.service
             └─689 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
```
Видим, что демон sshd запущен. Если соответствущего демона не оказалось, необходимо его установить: 
```shell
sudo apt install openssh-server
```
Генерируем пару публичный\приватный ключ:
```shell
vagrant@vagrant:~$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/vagrant/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/vagrant/.ssh/id_rsa
Your public key has been saved in /home/vagrant/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:zMScpgsz6or9dPxNj02Y/8fZUF/mpoNDYZdee6smzT4 vagrant@vagrant
The key's randomart image is:
+---[RSA 3072]----+
|                 |
|       o .       |
|        *      . |
|       *    o o =|
|    + . S  . + =+|
|   . = .   o. o.=|
|  . . +   +.+. ==|
|.o . . . o BoEoo+|
|o.o..   . o B=+o |
+----[SHA256]-----+
```

Копируем содержимое публичного ключа в authorized_keys:

```shell
vagrant@vagrant:~/.ssh$ more id_rsa.pub >> authorized_keys
```
Копируем приватный ключ с виртуальной vagrant машины на хостовую, вводим пароль:
```shell
dekar@Dekar-NIX:~/tmp$ scp -P 2222 vagrant@localhost:/home/vagrant/.ssh/id_rsa ~/
vagrant@localhost's password: 
id_rsa 
```
Пробуем подсоединиться с хостовой машины используя скопированный приватный ключ:

```shell
dekar@Dekar-NIX:~/tmp$ ssh vagrant@localhost -p 2222 -i ~/id_rsa
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 08 Dec 2021 09:05:35 PM UTC

  System load:  0.06              Processes:               119
  Usage of /:   3.2% of 61.31GB   Users logged in:         1
  Memory usage: 15%               IPv4 address for dummy0: 192.168.100.1
  Swap usage:   0%                IPv4 address for eth0:   10.0.2.15


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Wed Dec  8 21:02:26 2021 from 10.0.2.2
vagrant@vagrant:~$ 
```
Сессия установлена без ввода пароля пользователя vagrant. Следующим шагом можно запретить в конфиге /etc/ssh/sshd_config 
логины с использованием паролей установив для опции PasswordAuthentication значение no.

6. Создадим пару ключей для хостовой машины как в шаге 6 и скопируем в каталог пользователя vagrant приватный ключ:
```shell
dekar@Dekar-NIX:~/.ssh$ scp -P 2222 -i ~/id_rsa id_rsa vagrant@localhost:/home/vagrant/server.key
id_rsa 
```
В виртуальной машине создадим пользовательский ssh config следующего содержания:

```shell
Host dekar-nix 
    HostName 192.168.1.11
    IdentityFile ~/server.key
    User dekar
```
Пробуем подключиться к хостовой машине:
```shell
vagrant@vagrant:~/.ssh$ ssh dekar-nix
Enter passphrase for key '/home/vagrant/server.key': 
Welcome to KDE neon User - Plasma 25th Anniversary Edition (GNU/Linux 5.11.0-37-generic x86_64)
Last login: Thu Dec  9 21:39:51 2021 from 192.168.1.11
```
Соединение установлено по имени сервера!

7. Собираем дамп трафика для сетевого интерфейса WiFi утилитой tcpdump в формате pcap, 100 пакетов:

```shell
root@Dekar-NIX:~# tcpdump -i wlp3s0 -s 65535 -w ~/dump.pcap -c 100
tcpdump: listening on wlp3s0, link-type EN10MB (Ethernet), capture size 65535 bytes
100 packets captured
114 packets received by filter
0 packets dropped by kernel
```
Открытый файл представлен на скриншоте Wireshark.png
