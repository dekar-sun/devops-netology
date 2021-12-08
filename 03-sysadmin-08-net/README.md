1. Подключаемся к route-views.routeviews.org:

<details>
<summary>CLICK ME</summary>
<p>

```commandline
route-views>show ip route 5.167.196.122   
Routing entry for 5.167.196.0/22
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 7w0d ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 7w0d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 6939
      MPLS label: none
route-views>show bgp 5.167.196.122     
BGP routing table entry for 5.167.196.0/22, version 1015110026
Paths: (24 available, best #24, table default)
  Not advertised to any peer
  Refresh Epoch 1
  20912 3257 9002 9049 51570
    212.66.96.126 from 212.66.96.126 (212.66.96.126)
      Origin IGP, localpref 100, valid, external
      Community: 3257:8052 3257:50001 3257:54900 3257:54901 20912:65004 65535:65284
      path 7FE009EBD210 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 3
  3303 9002 9049 51570
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external
      Community: 3303:1004 3303:1007 3303:1030 3303:3067 9002:64667
      path 7FE104CDC6E8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7660 2516 1299 9049 51570
    203.181.248.168 from 203.181.248.168 (203.181.248.168)
      Origin incomplete, localpref 100, valid, external
      Community: 2516:1030 7660:9003
      path 7FE0CD38DE08 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3267 9049 51570
    194.85.40.15 from 194.85.40.15 (185.141.126.1)
      Origin incomplete, metric 0, localpref 100, valid, external
      path 7FE055A99E88 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  57866 9002 9049 51570
    37.139.139.17 from 37.139.139.17 (37.139.139.17)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 9002:0 9002:64667
      path 7FE0EE3D38E8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7018 1299 9049 51570
    12.0.1.63 from 12.0.1.63 (12.0.1.63)
      Origin incomplete, localpref 100, valid, external
      Community: 7018:5000 7018:37232
      path 7FE08F7FAC58 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3333 9002 9049 51570
    193.0.0.56 from 193.0.0.56 (193.0.0.56)
      Origin IGP, localpref 100, valid, external
      path 7FE04D791D30 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  49788 1299 9049 51570
    91.218.184.60 from 91.218.184.60 (91.218.184.60)
      Origin incomplete, localpref 100, valid, external
      Community: 1299:30000
      Extended Community: 0x43:100:1
      path 7FE0F23E2998 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  8283 1299 9049 51570
    94.142.247.3 from 94.142.247.3 (94.142.247.3)
      Origin incomplete, metric 0, localpref 100, valid, external
      Community: 1299:30000 8283:1 8283:101
      unknown transitive attribute: flag 0xE0 type 0x20 length 0x18
        value 0000 205B 0000 0000 0000 0001 0000 205B
              0000 0005 0000 0001 
      path 7FE04DDF7A58 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3356 9002 9002 9002 9002 9002 9049 51570
    4.68.4.46 from 4.68.4.46 (4.69.184.201)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:503 3356:903 3356:2067
      path 7FE09E10F8F8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  2497 1299 9049 51570
    202.232.0.2 from 202.232.0.2 (58.138.96.254)
      Origin incomplete, localpref 100, valid, external
      path 7FE1451F4DB8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1221 4637 9002 9049 51570
    203.62.252.83 from 203.62.252.83 (203.62.252.83)
      Origin IGP, localpref 100, valid, external
      path 7FE02617C9C0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  852 1299 9049 51570
    154.11.12.212 from 154.11.12.212 (96.1.209.43)
      Origin IGP, metric 0, localpref 100, valid, external
      path 7FE179043EC8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20130 6939 9049 51570
    140.192.8.16 from 140.192.8.16 (140.192.8.16)
      Origin IGP, localpref 100, valid, external
      path 7FE09F64F868 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  701 1299 9049 51570
    137.39.3.55 from 137.39.3.55 (137.39.3.55)
      Origin incomplete, localpref 100, valid, external
      path 7FE103EF7268 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3257 9002 9049 51570
    89.149.178.10 from 89.149.178.10 (213.200.83.26)
      Origin IGP, metric 10, localpref 100, valid, external
      Community: 3257:8052 3257:50001 3257:54900 3257:54901 65535:65284
      path 7FE149E99FC8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3549 3356 9002 9002 9002 9002 9002 9049 51570
    208.51.134.254 from 208.51.134.254 (67.16.168.191)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:503 3356:903 3356:2067 3549:2581 3549:30840
      path 7FE043FB2D98 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  53767 174 174 1299 9049 51570
    162.251.163.2 from 162.251.163.2 (162.251.162.3)
      Origin incomplete, localpref 100, valid, external
      Community: 174:21000 174:22013 53767:5000
      path 7FE045631CD0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  101 174 1299 9049 51570
    209.124.176.223 from 209.124.176.223 (209.124.176.223)
      Origin incomplete, localpref 100, valid, external
      Community: 101:20100 101:20110 101:22100 174:21000 174:22013
      Extended Community: RT:101:22100
      path 7FE0EA9D0448 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3561 3910 3356 9002 9002 9002 9002 9002 9049 51570
    206.24.210.80 from 206.24.210.80 (206.24.210.80)
      Origin IGP, localpref 100, valid, external
      path 7FE16D80D4A8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  4901 6079 9002 9002 9002 9002 9002 9049 51570
    162.250.137.254 from 162.250.137.254 (162.250.137.254)
      Origin IGP, localpref 100, valid, external
      Community: 65000:10100 65000:10300 65000:10400
      path 7FE0CEC75A90 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  19214 174 1299 9049 51570
    208.74.64.40 from 208.74.64.40 (208.74.64.40)
      Origin incomplete, localpref 100, valid, external
      Community: 174:21000 174:22013
      path 7FE0DE5194E8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1351 6939 9049 51570
    132.198.255.253 from 132.198.255.253 (132.198.255.253)
      Origin IGP, localpref 100, valid, external
      path 7FE15D854C78 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  6939 9049 51570
    64.71.137.241 from 64.71.137.241 (216.218.252.164)
      Origin IGP, localpref 100, valid, external, best
      path 7FE0509154E8 RPKI State not found
      rx pathid: 0, tx pathid: 0x0
```     
</p>
</details>

2. Создаём dummy интерфейс:
```commandline
oot@vagrant:~# modprobe -v dummy numdummies=1
insmod /lib/modules/5.4.0-80-generic/kernel/drivers/net/dummy.ko numdummies=0 numdummies=1
root@vagrant:~# lsmod | grep dummy
dummy                  16384  0
root@vagrant:~# ip link | grep dummy
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
```
Присваиваем ему IP адрес:
```commandline
root@vagrant:~# ip addr add 192.168.100.1/24 dev dummy0
root@vagrant:~# ip addr | grep dummy
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
    inet 192.168.100.1/24 scope global dummy0
```
Включаем интерфейс:
```commandline
root@vagrant:~# ip link set dummy0 up
root@vagrant:~# ip addr | grep dummy0
3: dummy0: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 192.168.100.1/24 scope global dummy0
```

Проверяем текущие маршруты:
```commandline
root@vagrant:~# ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
192.168.100.0/24 dev dummy0 proto kernel scope link src 192.168.100.1 
```
Добавляем статический маршрут:
```commandline
root@vagrant:~# ip route add 8.8.8.8 via 192.168.100.1
root@vagrant:~# ip route add 10.10.0.0/16 via 192.168.100.1
root@vagrant:~# ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
8.8.8.8 via 192.168.100.1 dev dummy0 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
10.10.0.0/16 via 192.168.100.1 dev dummy0 
192.168.100.0/24 dev dummy0 proto kernel scope link src 192.168.100.1 
```
По данным из последней команды видим, что добавлены два статических маршрута для адреса 8.8.8.8 и сети 10.10.0.0/16 через dummy интерфейс.

3. Проверяем открытые TCP порты в системе:
```commandline
root@vagrant:~# ss -tlpn
State    Recv-Q   Send-Q   Local Address:Port     Peer Address:Port    Process                                                                  
LISTEN   0        4096         127.0.0.1:8125          0.0.0.0:*        users:(("netdata",pid=631,fd=51))                                       
LISTEN   0        4096           0.0.0.0:19999         0.0.0.0:*        users:(("netdata",pid=631,fd=4))                                        
LISTEN   0        4096           0.0.0.0:111           0.0.0.0:*        users:(("rpcbind",pid=565,fd=4),("systemd",pid=1,fd=91))                
LISTEN   0        4096     127.0.0.53%lo:53            0.0.0.0:*        users:(("systemd-resolve",pid=566,fd=13))                               
LISTEN   0        128            0.0.0.0:22            0.0.0.0:*        users:(("sshd",pid=689,fd=3))                                           
LISTEN   0        4096             [::1]:8125             [::]:*        users:(("netdata",pid=631,fd=50))                                       
LISTEN   0        4096              [::]:111              [::]:*        users:(("rpcbind",pid=565,fd=6),("systemd",pid=1,fd=93))                
LISTEN   0        128               [::]:22               [::]:*        users:(("sshd",pid=689,fd=4)) 
```
Видим, что в данной системе прослушивается порт sshd демона, порт 53 DNS резолвера systemd-resolve, порт 111 демона rpcbind, 
порт 8125 перенаправлен в 19999 для внешних запросов сборщика метрик netdata.

4. Проверяем открытые в системе UDP сокеты:
```commandline
root@vagrant:~# ss -pua
State     Recv-Q   Send-Q   Local Address:Port     Peer Address:Port    Process                                                                 
UNCONN    0        0            127.0.0.1:8125          0.0.0.0:*        users:(("netdata",pid=631,fd=49))                                      
UNCONN    0        0        127.0.0.53%lo:domain        0.0.0.0:*        users:(("systemd-resolve",pid=566,fd=12))                              
UNCONN    0        0       10.0.2.15%eth0:bootpc        0.0.0.0:*        users:(("systemd-network",pid=406,fd=19))                              
UNCONN    0        0              0.0.0.0:sunrpc        0.0.0.0:*        users:(("rpcbind",pid=565,fd=5),("systemd",pid=1,fd=92))               
UNCONN    0        0                [::1]:8125             [::]:*        users:(("netdata",pid=631,fd=48))                                      
UNCONN    0        0                 [::]:sunrpc           [::]:*        users:(("rpcbind",pid=565,fd=7),("systemd",pid=1,fd=94))         
```
Видим, что порт 8125 так же используется демоном сбора мертик netdata, 127.0.0.53%lo:domain - очевидно используется DNS резолвером,
10.0.2.15%eth0:bootpc используется демоном systemd-network для получения сетевой конфигурации  посредством DHCP.

5. Конфигурация домашней сети представлена в файле MyNetwork.drawio.



