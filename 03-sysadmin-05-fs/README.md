1. sparse файлы это такие файлы в которых на уровне файловой системы высвобождаются области, занятые одними лишь нулями (0x00).
При этом реальное дисковое пространство выделяется тогда, когда вместо 0x00 записываются какие-то другие данные.
Разреженность (sparse) поможет сэкономить дисковое пространство только в таких файлах, в которых есть действительно большие пустые области.
Думаю технология отлично позволяет сэкономить место на файлах образов для ВМ.

2.Т.к. hardlink имеет тот же inode, что и "оригинальный" файл, то и права с файлом будут одни и те же.
Доказательство:
```buildoutcfg
dekar@Dekar-NIX:~/tmp$ ln file.txt file_hard.txt
dekar@Dekar-NIX:~/tmp$ ll -i
total 8
2228895 drwxrwxr-x  2 dekar dekar 4096 ноя 25 11:50 ./
1310721 drwxr-xr-x 29 dekar dekar 4096 ноя 24 17:09 ../
2229237 -rw-r--r--  2 dekar dekar    0 ноя 25 11:49 file_hard.txt
2229237 -rw-r--r--  2 dekar dekar    0 ноя 25 11:49 file.txt

```
3. Создана ВМ c двумя неразмеченными дисками sdb и sdc:
```buildoutcfg
vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
sdc                    8:32   0  2.5G  0 disk 
```
4. Созданы два раздела на sdb диске (fdisk -l):
```buildoutcfg
Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```
5. Разделы c sdb перенесены на sdc:
```buildoutcfg
sfdisk -d /dev/sdb|sfdisk /dev/sdc
fdisk -l
Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux
```
Общая картина разделов:
```buildoutcfg
root@vagrant:/home/vagrant# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
├─sdb1                 8:17   0    2G  0 part 
└─sdb2                 8:18   0    1K  0 part 
sdc                    8:32   0  2.5G  0 disk 
├─sdc1                 8:33   0    2G  0 part 
└─sdc2                 8:34   0    1K  0 part 
```
6. Собираем RAID1 на sdb1 и sdc1:
```buildoutcfg
root@vagrant:/home/vagrant# mdadm --create --verbose /dev/md/raid1 -l 1 -n 2 /dev/sd{b1,c1}
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 2094080K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md/raid1 started.
root@vagrant:/home/vagrant# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdb2                 8:18   0    1K  0 part  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdc2                 8:34   0    1K  0 part  
```
7. Собираем RAID0 на sdb2 и sdc2:
```buildoutcfg
root@vagrant:~# mdadm --create --verbose --force /dev/md/raid0 -l 0 -n 2 /dev/sd{b2,c2}
mdadm: chunk size defaults to 512K
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md/raid0 started.
root@vagrant:~# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdb2                 8:18   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdc2                 8:34   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
```
8. Создаём PV:
```buildoutcfg
root@vagrant:~# pvcreate /dev/md127 /dev/md126
  Physical volume "/dev/md127" successfully created.
  Physical volume "/dev/md126" successfully created.
```
9. Создаём общую Volume Group:
```buildoutcfg
root@vagrant:~# vgcreate vg1 /dev/md126 /dev/md127
  Volume group "vg1" successfully created
root@vagrant:~# vgdisplay
  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               <2.99 GiB
  PE Size               4.00 MiB
  Total PE              765
  Alloc PE / Size       0 / 0   
  Free  PE / Size       765 / <2.99 GiB
  VG UUID               uoMMkv-Nb1D-5JB5-uZ6V-dbBt-WDfg-ZMSLkw
```
10. Создаём LV размером 100 Мб на разделе md126 c RAID0
```buildoutcfg
root@vagrant:~# lvcreate -L 100M vg1 /dev/md126
  Logical volume "lvol0" created.
root@vagrant:~# lvs
  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lvol0  vg1       -wi-a----- 100.00m 
```
11. Создаём файловую систему ext4 на lvol0:
```buildoutcfg
root@vagrant:~# mkfs.ext4 /dev/vg1/lvol0
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```
12. Монтируем получившийся раздел в /mnt/new:
```buildoutcfg
root@vagrant:~# mkdir /mnt/new
root@vagrant:~# mount /dev/vg1/lvol0 /mnt/new
root@vagrant:~# df -h
Filesystem                  Size  Used Avail Use% Mounted on
udev                        447M     0  447M   0% /dev
tmpfs                        99M  712K   98M   1% /run
/dev/mapper/vgvagrant-root   62G  1.5G   57G   3% /
tmpfs                       491M     0  491M   0% /dev/shm
tmpfs                       5.0M     0  5.0M   0% /run/lock
tmpfs                       491M     0  491M   0% /sys/fs/cgroup
/dev/sda1                   511M  4.0K  511M   1% /boot/efi
tmpfs                        99M     0   99M   0% /run/user/1000
/dev/mapper/vg1-lvol0        93M   72K   86M   1% /mnt/new
```
13. Помещаем на раздел тестовый файл: 
```buildoutcfg
root@vagrant:~# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /mnt/new/test.gz.
--2021-11-25 11:14:09--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22538366 (21M) [application/octet-stream]
Saving to: ‘/mnt/new/test.gz.’

/mnt/new/test.gz.                         100%[====================================================================================>]  21.49M  8.07MB/s    in 2.7s    

2021-11-25 11:14:12 (8.07 MB/s) - ‘/mnt/new/test.gz.’ saved [22538366/22538366]
```
14. Вывод lsblk:
```buildoutcfg
root@vagrant:~# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdb2                 8:18   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
    └─vg1-lvol0      253:2    0  100M  0 lvm   /mnt/new
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
└─sdc2                 8:34   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
    └─vg1-lvol0      253:2    0  100M  0 lvm   /mnt/new
```
15. Целостность файла:
```buildoutcfg
root@vagrant:~# gzip -t /mnt/new/test.gz. ; echo $?
0
```
16. Перемещаем PV c RAID0 на RAID1 (c md126 на md127) и проверяем целостность ранее скаченного файла:
```buildoutcfg
root@vagrant:~# pvmove /dev/md126 /dev/md127
  /dev/md126: Moved: 92.00%
root@vagrant:~# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
│   └─vg1-lvol0      253:2    0  100M  0 lvm   /mnt/new
└─sdb2                 8:18   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md127              9:127  0    2G  0 raid1 
│   └─vg1-lvol0      253:2    0  100M  0 lvm   /mnt/new
└─sdc2                 8:34   0  511M  0 part  
  └─md126              9:126  0 1018M  0 raid0 
root@vagrant:~# gzip -t /mnt/new/test.gz. ; echo $?
0
```
17. Воспроизведение деградирования RAID1:
```buildoutcfg
root@vagrant:~# mdadm /dev/md127 --fail /dev/sdc1
mdadm: set /dev/sdc1 faulty in /dev/md127
```
18. Убеждаемся, что RAID1 на md127 работает в деградированном режиме:
```buildoutcfg
root@vagrant:~# dmesg | grep md127
[    4.313477] md/raid1:md127: active with 2 out of 2 mirrors
[    4.313493] md127: detected capacity change from 0 to 2144337920
[11382.392850] md/raid1:md127: Disk failure on sdc1, disabling device.
               md/raid1:md127: Operation continuing on 1 devices.
```
19. Тестируем скачанный файл:
```buildoutcfg
root@vagrant:~# gzip -t /mnt/new/test.gz. ; echo $?
0
```
Видим, что файл доступен и целостен. :)

20. Удаляем тестовую ВМ:
```buildoutcfg
dekar@Dekar-NIX:~/vagrant#2$ vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives.
```
