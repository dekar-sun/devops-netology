1. Команда "cd" вызывает системный вызов "chdir".
2. Судя по strace на моей системе база file находится в /usr/share/misc/magic.mgc: ```openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3```
3.1. Посмотреть командой  ```sudo lsof | grep deleted``` PID процесса, который пишет в удалённый файл и дескриптор открытого удалённого файла.
3.2. На данном этапе можно восстановить удалённый файл, если нужна информация в нём: ```cat /proc/$PID/fd/$descripter > file.log``` 
3.3. Далее можно занулить данный дескриптор: ```cat /dev/null > /proc/$PID/fd/$descripter```
3.4. Можно так же попытаться сделать редирект дескриптора открытого файла в другой дескриптор с помощью ```gdb```.
4. Зомби процессы не занимают ресурсов, но занимают место в таблице процессов, размер которой ограничен.
При достижении предельного количества записей в таблице все процессы пользователя, от имени которого выполняется создающий зомби родительский процесс, не будут способны создавать новые дочерние процессы.
5. При работе opensnoop открываются следующие файлы:
```
execve("/usr/sbin/opensnoop-bpfcc", ["/usr/sbin/opensnoop-bpfcc"], 0x7ffdcbe764e0 /* 31 vars */) = 0
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libutil.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libexpat.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/bin/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/localtime", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/python3.8", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
```
и т.д.

6. Судя по strace ```uname -a``` использует системный вызов uname. Цитата из man: "Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}."
Таким образом информацию о версии ядра и релизе ОС можно узнать из /proc/sys/kernel/osrelease и /proc/sys/kernel/version соответственно.
7. При использовании "&&", в случае если первая команда завершилась с кодом отличным от "0" вторая команда не будет выполнена.
При использовании ";" команды выполняются последовательно, в независимости от результата предыдущей.
Команда ```set -e``` завершает процесс шелла в котором выполняется, если какая либо последующая команда завершилась с кодом ошибки.
Так что, думаю нет смысла использовать ```set -e``` вместе с ```&&```.
8. Конструкция ```set -euxo pipefail```` состоит из следующих опций:
   1. -e выйти сразу при завершении любой команды с кодом отличным от "0"
   2. -u считать не заданные переменные как ошибки, с выводом в stderr
   3. -x выводит команды и их аргументы
   4. -o pipefail возвращает код возврата последовательности команд, ненулевой при выходе с ошибкой последней команды и нулевой при успешном выполнении всех команд.

Конструкция для сценария повышает детализацию вывода информации на экран или в лог файл, позволяет отладить сценарий.
Опция -e и -u позволяет добиться завершения сценария при ошибке и тем самым освобождает ресурсы системы.  
9. На моём окружении наиболее частый статус у процессов - S. Т.е. они находятся в режиме бездействия, в ожидании некоего события на вход.
Малая "l" означает многопоточный процесс (multi-threaded), "s" означает лидера сессии, т.е. процесс в сессии у которого PID=SID.
