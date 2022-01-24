
# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
1. Ускорение предоставления инфраструктуры для процессов разработки и тестирования, что позволяет ускорить процесс производства продукта и выхода на рынок.
2. Устранение дрейфа конфигурации объектов и как следствие идентичность конфигураций.
3. Более быстрый процесс разработки за счёт реализации непрерывной сборки продукта.
При этом уменьшается стоимость исправления дефекта, т.к. его можно обнаружить на каждом этапе сборки.

- Какой из принципов IaaC является основополагающим?
Основополагающим, на мой взгляд, является создание идемпотентного объекта инфраструктуры или операции.
Т.е. объекта идентичного тому, что уже существует.

## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
- Ansible не требует установки и настройки PKI окружения, а использует существующую SSH инфраструктуру.
Так же Ansible совмещает в себе декларативный и императивный подходы.
Не маловажным фактором является то, что Ansible позволяет создавать и использовать свои модули и конфигурации.

- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?
Pull больше подходит для управления большим количеством серверов и поддержанием на них идентичной конфигурации.
Но требует постоянно работающего сервера, который хранит конфигурации всех управляемых серверов. Т.к. в Pull модели соединение инициализируется управляемым сервером,
то существует сложность связанная с мониторингом применения конфигураций, особенно если их несколько.
Push лишён этого недостатка, но в нём имеется сложность в управлении большим кол-вом серверов, т.к. требует доступного подключения
к управляемому серверу в момент применения конфигурации, что не всегда возможно. Так же мастер сервер всегда должен знать о серверах, которыми он управляет.
Исходя из этого, осмелюсь сделать вывод, что наиболее гибкой и надёжной системой будет система совмещающая в себе оба метода.
Но скорее всего, такая система будет несколько более сложной в настройке.

## Задача 3

Установить на личный компьютер:

- VirtualBox
- Vagrant
- Ansible
*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*
Установленные версии ПО:
```commandline
dekar@Dekar-NIX:~/tmp$ vboxmanage --version
6.1.26_Ubuntur145957
dekar@Dekar-NIX:~/tmp$ vagrant --version
Vagrant 2.2.19
dekar@Dekar-NIX:~/tmp$ ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/dekar/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.
- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
```commandline
docker ps
```
Создан Vagrantfile:

```commandline
dekar@Dekar-NIX:~/vagrant#3$ cat Vagrantfile
ISO = "bento/ubuntu-20.04"
HOST_PREFIX = "ubuntu-server"
INVENTORY_PATH = "./ansible/inventory"

servers = [
  {
    :hostname => HOST_PREFIX + "01",
    :ssh_host => "2201",
    :ssh_vm => "22",
    :ram => 2048,
    :core => 2
  }
]

Vagrant.configure(2) do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false
  servers.each do |machine|
    config.vm.define machine[:hostname] do |node|
      node.vm.box = ISO
      node.vm.hostname = machine[:hostname]
      node.vm.network :forwarded_port, guest: machine[:ssh_vm], host: machine[:ssh_host]
      node.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
        vb.customize ["modifyvm", :id, "--cpus", machine[:core]]
        vb.name = machine[:hostname]
      end
      node.vm.provision "ansible" do |setup|
        setup.inventory_path = INVENTORY_PATH
        setup.playbook = "./ansible/provision.yml"
        setup.become = true
        setup.extra_vars = { ansible_user: 'vagrant' }
      end
    end
  end
end
```
В директории с Vagrantfile создан каталог ansible со следующим содержимым:

```commandline
dekar@Dekar-NIX:~/vagrant#3/ansible$ ll
total 24
drwxrwxr-x 3 dekar dekar 4096 янв 24 16:20 ./
drwxrwxr-x 4 dekar dekar 4096 янв 24 16:16 ../
-rw-rw-r-- 1 dekar dekar  161 янв 24 15:40 ansible.cfg
drwxrwxr-x 2 dekar dekar 4096 янв 24 16:31 group_vars/
-rw-rw-r-- 1 dekar dekar  101 янв 24 16:20 inventory
-rw-rw-r-- 1 dekar dekar  864 янв 24 15:39 provision.yml
```
Содержимое файлов:
```commandline
dekar@Dekar-NIX:~/vagrant#3/ansible$ cat ansible.cfg
[defaults]
inventory=./inventory
deprecation_warnings=False
command_warnings=False
host_key_checking = false
ansible_port=22
interpreter_python=/usr/bin/python3
dekar@Dekar-NIX:~/vagrant#3/ansible$ cat inventory
[nodes:children]
vagrant_vms

[vagrant_vms]
ubuntu-server01 ansible_host=127.0.0.1 ansible_port=2201
dekar@Dekar-NIX:~/vagrant#3/ansible$ cat group_vars/vagrant_vms
ansible_user: vagrant
ansible_password: vagrant
dekar@Dekar-NIX:~/vagrant#3/ansible$ cat provision.yml
---

  - hosts: nodes
    become: yes
    become_user: root
    remote_user: vagrant

    tasks:
      - name: Create directory for ssh-keys
        file: state=directory mode=0700 dest=/root/.ssh/

      - name: Adding rsa-key in /root/.ssh/authorized_keys
        copy: src=~/.ssh/id_rsa.pub dest=/root/.ssh/authorized_keys owner=root mode=0600
        ignore_errors: yes

      - name: Checking DNS
        command: host -t A docker.com

      - name: Installing tools
        package: >
          package={{ item }}
          state=present
          update_cache=yes
        with_items:
          - git
          - curl

      - name: Installing docker
        shell: curl -fsSL get.docker.com -o get-docker.sh && chmod +x get-docker.sh && ./get-docker.sh

      - name: Add the current user to docker group
        user: name=vagrant append=yes groups=docker
```

После отработки vagrant up проверяем версию docker:
```commandline
dekar@Dekar-NIX:~/vagrant#3$ vagrant ssh
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 24 Jan 2022 02:04:07 PM UTC

  System load:  0.08              Processes:                110
  Usage of /:   3.2% of 61.31GB   Users logged in:          0
  Memory usage: 11%               IPv4 address for docker0: 172.17.0.1
  Swap usage:   0%                IPv4 address for eth0:    10.0.2.15


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Mon Jan 24 13:36:22 2022 from 10.0.2.2
vagrant@ubuntu-server01:~$ docker --version
Docker version 20.10.12, build e91ed57
vagrant@ubuntu-server01:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
После развёртывания сервера можно управлять им с помощью скопированного ssh ключа, используя ansible_user=root в inventory файле, или в глобальных переменных.




