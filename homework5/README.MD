# Домашняя работа 5

## Анализ логов

Скрипты анализа логов **nginx** реализованы на **Python** и **Bash**.  
Кроме того, используя флаг запуска **--json** - разбор логов, согласно заданию - будет представлен в формате **JSON**. Скрипт
на **Python** осуществляет вывод в указанные в коде файлы **.txt** и **.json**. Скрипт на **Bash** выводит результат анализа в
консоль, однако результат его работы можно перенаправить в заданный файл, используя оператор перенаправления вывода **>**.

### Логика работы скриптов

#### Bash

1. #### Total requests

Выводим содержимое файла с логами построчно, используя **cat** и с помощью **pipe - |** перенаправляем результат вывода команде **
grep**, которая выбирает только те строки, в которых существует какой-либо
**HTTP-запрос**. Далее просто перенаправляем результат команде **wc** с ключом **-l**, которая считает кол-во строк, переданной
ей.  
С помощью команды **echo** выводим результат в консоль

2. #### Total requests by type

Аналогично предыдущему пункту, однако рассматриваем каждый **HTTP-запрос**
отдельно.  
Затем выводим результат на печать с помощью команды **echo**.

3. #### Top 10 requests by usage

Так же выводим содержимое файла с логами построчно, используя **cat**, далее преобразуем вывод чередой команд, используя **pipe -
|**: **cut -d** - вырезаем нужную информацию из текста, использую заданный
**delimeter (разделитель)**; используем команду **sort** для последующей корректной работы команды **uniq**; командой **uniq** с
ключом **-c** - вычисляем кол-во повторений каждой строки; с помощью команды **sort -k1 -nr** с указанными ключами (**r-reverse**
и
**n**-используется для сравнения чисел) - сортируем по первой колонке (**k1**), то есть по результату работы команды **uniq -c**;
окончательно с помощью команды
**head -10** - извлекаем 10 верних результатов, то есть имеющих наибольшее значение в колонке 1.  
Выводим результат на печать с помощью команды **echo**.

4. #### Top 5 requests by response size ended with 4** error

Логика похожа на прошлый пункт, однако здесь используем более мощную утилиту для работы с текстом/извлечения данных - **awk**.
Данная команда сама разбивает данные по некоторому сепаратору (по умолчанию - пробел), представляя таким образом их в табличном
виде.  
Используя конструкцию **'$номер колонки ~ /<регулярное выражение>/'** извлекаем только те, строки, что удовлетворяют условию (
клиентская ошибка). Затем с помощью
**'{print $номер колонки}'** - печатаем все необходимые колонки и так же с помощью
**sort -k3 -nr** - сортируем по необходимому столбцу и, наконец, - с помощью
**head -5** - извлекаем 5 верних результатов, то есть имеющих наибольшее значение в колонке 3.  
Выводим результат на печать с помощью команды **echo**.

5. #### Top 5 users by count of requests ended with 5** error

В целом аналогичная логика - только приемы используются как из 3 пункта, так и из 4: задаем регулярное выражение, согласно
заданию; используем команду **sort** для последующей корректной работы команды **uniq**; командой **uniq** с ключом **-c** -
вычисляем кол-во повторений каждой строки; **sort -k1 -nr** - сортируем по необходимому столбцу и, наконец, - с помощью
**head -5** - извлекаем 5 верних результатов, то есть имеющих наибольшее значение в колонке 1. Выводим результат на печать с
помощью команды **echo**.

#### Python

Не вижу необходимости расписывать подробно логику парсинга. Основной принцип - заменить команды unix-систем для работы с текстом
на аналогичные встроенные инструменты языка **Python**. Весь используемый функционал языка - встроенные функции для работы со
строками и стандартная библиотека **re** для работы с регулярными выражениями. Для преобразования результата парсинга в **JSON**
используется стандартная библиотека **json**.  
Для большего удобства - был разработан класс **BaseParser**, аккумулирующий в себе всю необходимую логику.  
Сам парсинг (вызов методов класса), осуществлялся в стороннем скрипте, путем создания объекта класса **BaseParser** и последующего
вызова его методов.

### Выводы

В целом решение и на **Python**, и на **Bash** - имеют место быть. Однако, очевидно, что на **Bash** - оно гораздо проще и
элегантее. Инструменты анализа **Python** более простые, но менее эффективные, периодически есть необходимость реализовать что-то
самостоятельно, что нельзя сказать о
**Bash**.  
Считаю, что необходимо уметь грамотно использовать оба средства, так как ситуации и потребности бывают разные. Тем не менее,
склоняюсь к мнению - что для анализа сложных логов целесообразнее использовать **Bash**, а для анализа и парсинга небольшой
информации (которая может быть использована в разработке, например: данные для авто-тестов) - лучше использовать средства языка
разработки, то есть **Python**.
