5. По умолчанию vargant создал машину со следующими характеристиками: CPU 2, MEMORY 1024 Mb, HDD 64 Gb
6. Чтобы увеличить оперативной памяти или ресурсов процессора виртуальной машине необходимо добавить в файл Vagrantfile строчки 
```
   config.vm.provider "virtualbox" do |v|
     v.memory = 2048
     v.cpus = 4
   end
```
Таким образом Vagrantfile будет выглядеть таким образом:
```
Vagrant.configure("2") do |config|
        config.vm.box = "bento/ubuntu-20.04"
          config.vm.provider "virtualbox" do |v|
            v.name = "ubuntu_20.04"
            v.memory = 2048
            v.cpus = 4
          end
 end
```
Далее выполнить vagrant reload, если машина была включена.
8. Длина журнала history хранится в переменной $HISTSIZE - 703 строка man bash. Так же, судя по man bash, на длину истории, хранимой после закрытия терминала влияет переменная $HISTFILESIZE - 699 строка в man.
Описание ignoreboth находится на 692 строке man. И служит для отключения сохранения в истории строк, начинающихся со знака пробела и строк, совпадающих с последней выполненной командой. 
Таким образом она объединяет в себе две директивы ignorespace и ignoredups.
9. Согласно строке 156 {} применяются в сценариях со следующими командами: do done elif else esac fi for function if in select then until while.
Так же, согласно, строке 889 {} применяется для замены выражений в фигурных скобках.
10. Создать 100000 файлов можно командой touch так: touch file{0..100000}.txt
В моём случае не получилось создать ни 100000 ни 300000 такой командой, т.к. превышен предел ARG_MAX: 
getconf ARG_MAX
2097152
В этом случае для создания большого количества файлов можно использовать цикл for.
11. Конструкция [[ -d /tmp ]] определяет, существует ли файл tmp и является ли он каталогом.
12. Добавление пути bash is /tmp/new_path_directory/bash первым в список:
vagrant@vagrant:~/tmp$ mkdir /tmp/new_path_directory
vagrant@vagrant:~/tmp$ cp /usr/bin/bash /tmp/new_path_directory/
vagrant@vagrant:~/tmp$ PATH=/tmp/new_path_directory/:$PATH
vagrant@vagrant:~/tmp$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /usr/bin/bash
bash is /bin/bash
13. Команда at используется для назначения одноразового задания на заданное время, а команда batch — для назначения группы одноразовых задач. 