# Домашнее задание к занятию «2.4. Инструменты Git»

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.
* git show aefea
* Полный хэш - aefead2207ef7e2aa5dc81a34aedf0cad4c32545
* Комментарий - Update CHANGELOG.md
2. Какому тегу соответствует коммит `85024d3`?
* git log --oneline --all | grep 85024d3
* Тег - v0.12.23
3. Сколько родителей у коммита `b8d720`? Напишите их хеши.
* b8d720 - мерж коммит с двумя родителями 56cd7859e и 9ea88f22f
* git show --parents b8d720
* git log b8d720 -10 --pretty=format:'%h %s' --graph 

4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.
* git log v0.12.23..v0.12.24 --pretty=format:'%h %s'
33ff1c03b v0.12.24
b14b74c49 [Website] vmc provider links
3f235065b Update CHANGELOG.md
6ae64e247 registry: Fix panic when server is unreachable
5c619ca1b website: Remove links to the getting started guide's old location
06275647e Update CHANGELOG.md
d5f9411f5 command: Fix bug when using terraform login on Windows
4b6d06cc5 Update CHANGELOG.md
dd01a3507 Update CHANGELOG.md
225466bc3 Cleanup after v0.12.23 release

5. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит 
так `func providerSource(...)` (вместо троеточия перечислены аргументы).
* git grep -n 'func providerSource' 
* git log -L:'func providerSource':provider_source.go --oneline или git log -S'func providerSource' --oneline
* Коммит в котором создана функция - 8c928e835
7. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.
* git grep 'func globalPluginDirs'
* git log -L:'globalPluginDirs':plugins.go --oneline
* Коммиты в которых была изменена функция: 78b122055 52dbf9483
* Функция была создана в коммите 8364383c3
8. Кто автор функции `synchronizedWriters`? 
* git log -SsynchronizedWriters
* git show 5ac311e2a91e381e2f52234668b49ba670aa0fe5
* Судя по логу функция была добавлена в вышеприведённом коммите а его автор - Martin Atkins. 