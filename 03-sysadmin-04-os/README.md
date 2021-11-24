1. Установлен node_exporter и доступен на 9100 порту.

Сервис останавливается и стартует корректно:
```buildoutcfg
dekar@Dekar-NIX:~/DevOps/devops-netology/03-sysadmin-04-os$ sudo systemctl stop node_exporter.service
[sudo] password for dekar: 
dekar@Dekar-NIX:~/DevOps/devops-netology/03-sysadmin-04-os$ systemctl -a | grep node_exporter
dekar@Dekar-NIX:~/DevOps/devops-netology/03-sysadmin-04-os$ sudo systemctl start node_exporter.service
dekar@Dekar-NIX:~/DevOps/devops-netology/03-sysadmin-04-os$ sudo systemctl status node_exporter.service
● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-11-24 15:43:15 MSK; 10s ago
   Main PID: 96570 (node_exporter)
      Tasks: 5 (limit: 18726)
     Memory: 2.4M
     CGroup: /system.slice/node_exporter.service
             └─96570 /usr/local/bin/node_exporter

ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=thermal_zone
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=time
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=timex
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=udp_queues
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=uname
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=vmstat
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=xfs
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:115 level=info collector=zfs
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=node_exporter.go:199 level=info msg="Listening on" address=:9100
ноя 24 15:43:15 Dekar-NIX node_exporter[96570]: ts=2021-11-24T12:43:15.858Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
```

Также для node_esporter прописан unit-файл:
```buildoutcfg
more /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter
EnvironmentFile=/etc/default/node_exporter

[Install]
WantedBy=multi-user.target
```
При этом переменные с /etc/default/node_exporter подхватываются (PATH=$PATH:'Hello!):
```buildoutcfg
dekar@Dekar-NIX:~$ ps -e | grep node_exporter
  98011 ?        00:00:00 node_exporter
dekar@Dekar-NIX:~$ sudo cat /proc/98011/environ
LANG=en_US.UTF-8LC_ADDRESS=ru_RU.UTF-8LC_IDENTIFICATION=ru_RU.UTF-8LC_MEASUREMENT=ru_RU.UTF-8LC_MONETARY=ru_RU.UTF-8LC_NAME=ru_RU
.UTF-8LC_NUMERIC=ru_RU.UTF-8LC_PAPER=ru_RU.UTF-8LC_TELEPHONE=ru_RU.UTF-8LC_TIME=ru_RU.UTF-8PATH=$PATH:'Hello!
'XDG_DATA_DIRS=/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/HOME=/home/node_exporterLOGNAME=node_exporter
USER=node_exporterINVOCATION_ID=a4ee02e1b2fd47f88e06c84a117f628dJOURNAL_STREAM=8:641038dekar@Dekar-NIX:~$ 
```
2. Для базового мониторинга хоста по CPU, памяти, диску и сети можно выбрать следующие опции:
    CPU (для каждого ядра\процессора):
```buildoutcfg
node_cpu_seconds_total{cpu="0",mode="idle"} 645543.97
node_cpu_seconds_total{cpu="0",mode="iowait"} 1394.26
node_cpu_seconds_total{cpu="0",mode="irq"} 0
node_cpu_seconds_total{cpu="0",mode="nice"} 176.28
node_cpu_seconds_total{cpu="0",mode="softirq"} 28.13
node_cpu_seconds_total{cpu="0",mode="steal"} 0
node_cpu_seconds_total{cpu="0",mode="system"} 6818.14
node_cpu_seconds_total{cpu="0",mode="user"} 12675.03
```
RAM:
```buildoutcfg
node_memory_MemAvailable_bytes 9.919565824e+09
node_memory_MemFree_bytes 3.789176832e+09
node_memory_SwapCached_bytes 0
node_memory_SwapFree_bytes 1.7179947008e+10
node_memory_SwapTotal_bytes 1.7179947008e+10
```
DISK (возможно для каждого диска в системе):
```buildoutcfg
node_disk_io_now{device="sda"} 0
node_disk_io_now{device="sdb"} 0
node_disk_read_time_seconds_total{device="sda"} 233.064
node_disk_read_time_seconds_total{device="sdb"} 546.764
node_disk_write_time_seconds_total{device="sda"} 409.704
node_disk_write_time_seconds_total{device="sdb"} 5455.0070000000005
```
Network (для каждого сетевого адаптера):
```buildoutcfg
node_network_receive_bytes_total{device="enp0s25"} 0
node_network_receive_bytes_total{device="lo"} 9.786265e+06
node_network_receive_bytes_total{device="wlp3s0"} 1.162112924e+09
node_network_receive_drop_total{device="enp0s25"} 0
node_network_receive_drop_total{device="lo"} 0
node_network_receive_drop_total{device="wlp3s0"} 11007
node_network_receive_errs_total{device="enp0s25"} 0
node_network_receive_errs_total{device="lo"} 0
node_network_receive_errs_total{device="wlp3s0"} 0
node_network_transmit_bytes_total{device="enp0s25"} 0
node_network_transmit_bytes_total{device="lo"} 9.786265e+06
node_network_transmit_bytes_total{device="wlp3s0"} 1.93036827e+08
node_network_transmit_drop_total{device="enp0s25"} 0
node_network_transmit_drop_total{device="lo"} 0
node_network_transmit_drop_total{device="wlp3s0"} 0
node_network_transmit_errs_total{device="enp0s25"} 0
node_network_transmit_errs_total{device="lo"} 0
node_network_transmit_errs_total{device="wlp3s0"} 0
```
3. Netdata установлена, порт 19999 проброшен с виртуальной машины на хостовую.
На хостовой машине:
```buildoutcfg
sudo lsof -i :19999
COMMAND     PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
GeckoMain  1786 dekar  128u  IPv4 651227      0t0  TCP localhost:56352->localhost:19999 (ESTABLISHED)
GeckoMain  1786 dekar  140u  IPv4 651228      0t0  TCP localhost:56354->localhost:19999 (ESTABLISHED)
GeckoMain  1786 dekar  154u  IPv4 653453      0t0  TCP localhost:56356->localhost:19999 (ESTABLISHED)
VBoxHeadl 99633 dekar   21u  IPv4 647734      0t0  TCP *:19999 (LISTEN)
VBoxHeadl 99633 dekar   26u  IPv4 653451      0t0  TCP localhost:19999->localhost:56352 (ESTABLISHED)
VBoxHeadl 99633 dekar   27u  IPv4 653452      0t0  TCP localhost:19999->localhost:56354 (ESTABLISHED)
VBoxHeadl 99633 dekar   29u  IPv4 653454      0t0  TCP localhost:19999->localhost:56356 (ESTABLISHED)
```
На виртуальной машине:
```buildoutcfg
sudo lsof -i :19999
COMMAND PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
netdata 627 netdata    4u  IPv4  22978      0t0  TCP *:19999 (LISTEN)
netdata 627 netdata   24u  IPv4  29724      0t0  TCP vagrant:19999->_gateway:56414 (ESTABLISHED)
netdata 627 netdata   28u  IPv4  29731      0t0  TCP vagrant:19999->_gateway:56420 (ESTABLISHED)
netdata 627 netdata   50u  IPv4  29347      0t0  TCP vagrant:19999->_gateway:56356 (ESTABLISHED)
```
4. По выводу dmesg однозначно можно понять, что ОС запущена на виртуальном оборудовании. 
Например:
```buildoutcfg
vagrant@vagrant:~$ dmesg | grep -i virtual
[    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[    0.001839] CPU MTRRs all blank - virtualized system.
[    0.090023] Booting paravirtualized kernel on KVM
[    4.243729] systemd[1]: Detected virtualization oracle.
```
Тут интересна строчка "Booting paravirtualized kernel on KVM", что означает что ОС запущена на гипервизоре KVM. 
Так же systemd определил, что система запущена на виртуальной среде oracle: "systemd[1]: Detected virtualization oracle."

5. Максимальное число открытых дескрипторов для ядра ОС в моей виртуальной машине:
```buildoutcfg
vagrant@vagrant:~$ sysctl -n fs.nr_open
1048576
```
Данное число кратно 1024. В данном случае это 1024х1024.
Судя по ```ulimit --help``` существуют так называемые мягкие лимиты (касательно открытых файловых дескрипторов: ```ulimit -Sn```) и жёсткие
лимиты ```ulimit -Hn```.  При этом мягкий лимит процесс может увеличить в процессе своей работы, а жёсткий лимит - ограничен 
системным значением "fs.nr_open", но при этом может быть уменьшен. 

6. Ответ:
```buildoutcfg
root@vagrant:~# unshare -fp --mount-proc sleep 1h &
[1] 1207
root@vagrant:~# ps -e | grep sleep
   1208 pts/0    00:00:00 sleep
root@vagrant:~# nsenter --target 1208 --pid --mount
root@vagrant:/# ps -a
    PID TTY          TIME CMD
      1 pts/0    00:00:00 sleep
      2 pts/0    00:00:00 bash
     11 pts/0    00:00:00 ps
root@vagrant:/# 
```
7. Запись ```:(){ :|:& };:``` можно трансформировать в более читаемый вид, например:
```buildoutcfg
func()
{
    func | func &
};
func
```
Таким образом мы создаём функцию с именем func в теле которой происходит двойное порождение себя (через pipe) и создание 
фонового процесса. После вызова такой функции каждый экземпляр func запускает два новых func и так далее, образуя своеобразное дерево процессов.
В dmesg можно при этом видеть такую строчку ```cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-1.scope``` 
Т.е. функция столкнулась с лимитом pid для пользователя с id 1000, под которым она была запущена.
А команда ```systemctl status user-1000.slice | grep limit``` покажет текущий лимит pid:
```buildoutcfg
root@vagrant:/# systemctl status user-1000.slice | grep limit
      Tasks: 13 (limit: 5014)
             │ └─37897 grep --color=auto limit
root@vagrant:/#
```
Этот же параметр для конкретного пользователя можно посмотреть так:
```buildoutcfg
root@vagrant:~# cat /sys/fs/cgroup/pids/user.slice/user-1000.slice/pids.max
5014
```
При этом в сессии можно ограничить количество процессов с помощью ```ulimit -u 100```
При этом количество процессов ограничивается до 100 для текущей сессии.
В этом случае максимальное доступное пользователю количество процессов будет меньше чем максимальное количество доступных
пользователю pid и выполнение форк-бомбы (функции func()) должно завершиться быстрее и не приводить к значительному расходу ресурсов системы. 

