# Повальная книга фуков

Основная причина создания FunC Cookbook - собрать весь опыт у разработчиков FunC в одном месте, чтобы будущие разработчики могли использовать его!

По сравнению с [Документацией по FunC](/v3/documentation/smart-contracts/func/docs/types), эта статья больше посвящена повседневным задачам, решаемым разработчиком FunC при разработке смарт-контрактов.

## Основы

### Как написать оператор "если"

Допустим, мы хотим проверить, является ли какое-либо событие актуальным. Для этого мы используем переменную флага. Помните, что в FunC `true` это `-1` и `false` это `0`.

```func
int флаг = 0; ;; false

if (flag) { 
    ;; сделать что-то
}
else {
    ;; отклонить транзакцию
}
```

> 💡 Замечено
>
> Нам не нужен оператор `==`, потому что значение `0` является `false`, поэтому любое другое значение будет `true`.

> 💡 Полезные ссылки
>
> ["Если выражение" в документах](/v3/documentation/smart-contracts/func/docs/statements#if-statements)

### Как написать цикл повтора

В качестве примера мы можем принять экспоненции

```func
int number = 2;
int multiplier = number;
int degree = 5;

repeat(degree - 1) {

    number *= multiplier;
}
```

> 💡 Полезные ссылки
>
> ["Повторить цикл" в документах](/v3/documentation/smart-contracts/func/docs/statements#repeat-loop)

### Как написать цикл "пока"

Хотя это полезно, когда мы не знаем, как часто выполнять определенные действия. Например, возьмите «клетку», известную хранить до четырех ссылок на другие ячейки.

```func
cell inner_cell = begin_cell() ;; создайте новый пустой конструктор
        . tore_uint(123, 16) ;; храните uint со значением 123 и длиной 16 бит
        . nd_cell(); ;; convert builder to a cell

cell message = begin_cell()
        . tore_ref(inner_cell) ;; сохранить ячейку как ссылку
        . tore_ref(inner_cell)
        .end_cell();

Slice msg = message.begin_parse(); ;; convert cell to slice
while (msg. lice_refs_empty?() ! -1) { ;; следует напомнить, что -1 истинная
    ячейка inner_cell = msg~load_ref(); ;; Загрузите ячейку из срез msg
    ;; сделайте что-то
}
```

> 💡 Полезные ссылки
>
> ["Цикл пока" в документах](/v3/documentation/smart-contracts/func/docs/statements#while-loop)
>
> ["Гены" в документах](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage)
>
> ["slice_refs_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#slice_refs_empty)
>
> ["store_ref()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### Как написать до цикла

Когда нам нужен цикл, чтобы запустить хотя бы один раз, мы используем `do until`.

```func
int флаг = 0;

do {
    ;; сделать что-то, что флаг является ложным (0) 
} до тех пор, пока (флаг == -1); ;; -1 верно
```

> 💡 Полезные ссылки
>
> ["До цикла" в документах](/v3/documentation/smart-contracts/func/docs/statements#until-loop)

### Как определить пустой кусочек

Прежде чем работать с `slice`, необходимо проверить, есть ли у него какие-либо данные для корректной обработки. Мы можем использовать `slice_empty? )` для этого, но мы должны учитывать, что он вернёт `0` (`false`), если есть хотя бы один `bit` данных или один `ref`.

```func
;; Создание пустой маски
маски empty_slice = "";
;; `slice_empty?()` возвращает `true`, потому что маска не имеет `bits` и `refs`
empty_slice. lice_empty?();

;; создание маски, содержащей только биты
slice_with_bits_only = "Hello, world! ;
;; `slice_empty?()` возвращает `false`, потому что у маски есть любые `bits`
slice_with_bits_only. lice_empty?();

;; создание кусочека, содержащего только
кусочек slice_with_refs_only = begin_cell()
    . tore_ref(null())
    . nd_cell()
    .begin_parse();
;; `slice_empty?()` возвращает `false`, так как у кусочек есть любой `refs`
slice_with_refs_only. lice_empty?();

;; создание маски, содержащей биты и рефералы
ломтиков slice_with_bits_and_refs = begin_cell()
    . tore_slice("Привет, мир!")
    .store_ref(null())
    .end_cell()
    . egin_parse();
;; `slice_empty?()` возвращает `false`, потому что у маски есть любые `bits` и `refs`
slice_with_bits_and_refs.slice_empty?();
```

> 💡 Полезные ссылки
>
> ["slice_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#slice_empty)
>
> ["store_slice()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> ["store_ref()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### Как определить, является ли маска пустой (нет битов, но может иметь ответ)

Если нам нужно проверить только `bits` и не важно, есть ли в `slice`, тогда нам следует использовать `slice_data_empty?()`.

```func
;; Создание пустой маски
маски empty_slice = "";
;; `slice_data_empty?()` возвращает `true`, поскольку у маски нет `bits`
empty_slice. lice_data_empty?();

;; создание фрагмента, содержащего только биты
ломки slice_with_bits_only = "Hello, world! ;
;; `slice_data_empty?()` возвращает `false`, потому что у маски есть любой `bits`
slice_with_bits_only. lice_data_empty?();

;; создание маски, содержащей только
маску slice_with_refs_only = begin_cell()
    . tore_ref(null())
    . nd_cell()
    .begin_parse();
;; `slice_data_empty?()` возвращает `true`, так как в маске нет `bits`
slice_with_refs_only. lice_data_empty?();

;; создание маски, содержащей биты и рефералы
маски slice_with_bits_and_refs = begin_cell()
    . tore_slice("Привет, мир!")
    .store_ref(null())
    .end_cell()
    . egin_parse();
;; `slice_data_empty?()` возвращает `false`, так как в маске есть любые `bits`
slice_with_bits_and_refs.slice_data_empty?();
```

> 💡 Полезные ссылки
>
> ["slice_data_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#slice_data_empty)
>
> ["store_slice()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> ["store_ref()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### Как определить, является ли маска пустой (нет рефералов, но может иметь биты)

Если мы заинтересованы только в `refs`, мы должны проверить их присутствие с помощью `slice_refs_empty?()`.

```func
;; creating empty slice
slice empty_slice = "";
;; `slice_refs_empty?()` returns `true`, because slice doesn't have any `refs`
empty_slice.slice_refs_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_refs_empty?()` returns `true`, because slice doesn't have any `refs`
slice_with_bits_only.slice_refs_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_refs_only.slice_refs_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_bits_and_refs.slice_refs_empty?();
```

> 💡 Полезные ссылки
>
> ["slice_refs_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#slice_refs_empty)
>
> ["store_slice()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> ["store_ref()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### Как определить пустую ячейку

Чтобы проверить, есть ли данные в ячейке, мы должны сначала преобразовать их в `slice`. Если нам интересно только иметь `bits`, мы должны использовать `slice_data_empty?()`, если только `refs` - `slice_refs_empty?()`. В случае, если мы хотим проверить наличие любых данных, независимо от того, является ли это бит или `ref`, нам нужно использовать `slice_empty?()`.

```func
ячейка_with_bits_and_refs = begin_cell()
    .store_uint(1337, 16)
    .store_ref(null())
    . nd_cell();

;Измените тип `cell` для маски `begin_parse()`
маски cs = cell_with_bits_and_refs. egin_parse();

;; определяет, является ли маска пустой
если (сs. lice_empty )) {
    ;; клетка пустая
}
else {
    ; ячейка не пустая
}
```

> 💡 Полезные ссылки
>
> ["slice_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#slice_empty)
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["store_uint()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### Как определить, если dict пуст

Существует метод `dict_empty?()`, чтобы проверить наличие данных в dict. Этот метод эквивалентен `cell_null?()`, потому что обычно 'null\`-cell является пустой словарь.

```func
ячейка d = new_dict();
d~udict_set(256, 0, "hello");
d~udict_set(256, 1, "world");

if (d. пропущено? )) { ;; Определите, если dict пустой
    ;; dict является пустым
}
else {
    ;; dict не пустой
}
```

> 💡 Полезные ссылки
>
> ["dict_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#dict_empty)
>
> ["new_dict()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#new_dict)
>
> ["dict_set()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_set) добавляя некоторые элементы в dict с функцией, так что это не пустой

### Как определить, является ли трубка пустой

При работе с 'tuples' всегда важно знать, являются ли значения внутри для извлечения. Если мы попытаемся извлечь значение из пустой «tuple», то получаем ошибку: «Не допустимый размер» с кодом `exit 7`.

```func
;; Объявить функцию tlen, потому что она не представлена в stdlib
(int) tlen (tuple t) как "TLEN";

() main () {
    tuple t = empty_tuple();
    t~tpush(13);
    t~tpush(37);

    if (t. len() == 0) {
        ;; tuple является пустым
    }
    else {
        ; трубка не пустая
    }
}
```

> 💡 Замечено
>
> Функция сборки разделена на несколько частей. You can read more [here](/v3/documentation/smart-contracts/func/docs/functions#assembler-function-body-definition) and see [list of all assembler commands](/v3/documentation/tvm/instructions).

> 💡 Полезные ссылки
>
> ["empty_tuple?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#empty_tuple)
>
> ["tpush()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#tpush)
>
> ["Выйти кода" в документах](/v3/documentation/tvm/tvm-exit-codes)

### Как определить пустой список стилей lisp

```func
тузовые числа = null();
чисел = cons(100, числа);

если (числа. ull?()) {
    ;; list-style list is empty
} else {
    ; список стилей не пустой
}
```

Мы добавляем номер 100 в наш список стилей с помощью функции [cons](/v3/documentation/smart-contracts/func/docs/stdlib/#cons), так что она не пуста.

### Как определить состояние контракта пустое

Скажем, у нас есть «счет», который хранит количество транзакций. Эта переменная недоступна во время первой транзакции в состоянии смарт-контракта поскольку состояние пусто, поэтому необходимо обработать такой случай. Если состояние пустое, мы создаем переменную «счетчик» и сохраним ее.

```func
;; `get_data()` will return the data cell from contract state
cell contract_data = get_data();
slice cs = contract_data.begin_parse();

if (cs.slice_empty?()) {
    ;; contract data is empty, so we create counter and save it
    int counter = 1;
    ;; create cell, add counter and save in contract state
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
else {
    ;; contract data is not empty, so we get our counter, increase it and save
    ;; we should specify correct length of our counter in bits
    int counter = cs~load_uint(32) + 1;
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
```

> 💡 Замечено
>
> Мы можем определить пустое состояние контракта, определив что [ячейка пуста](/v3/documentation/smart-contracts/func/cookbook#how-to-determine-if-cell-is-empty).

> 💡 Полезные ссылки
>
> ["get_data()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#get_data)
>
> ["begin_parse()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#begin_parse)
>
> ["slice_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_empty)
>
> ["set_data?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#set_data)

### Как построить внутреннюю ячейку сообщения

Если мы хотим, чтобы контракт послал внутреннее сообщение, мы должны сначала правильно создать его в ячейке, указание технических флагов, адреса получателя и остальных данных.

```func
;; Мы используем литерал `a`, чтобы получить действительный адрес внутри строки, содержащей адрес 
добавление маски = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
;; мы используем `op` для идентификации операций
int op = 0;

ячейка msg = begin_cell()
    . tore_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(op, 32)
.end_cell();

send_raw_message(msg, 3); ;; режим 3 - Оплата сборов отдельно и игнорирование ошибок 
```

> 💡 Замечено
>
> В этом примере мы используем букву `a` для получения адреса. Вы можете найти больше о строковых буквах в [docs](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)

> 💡 Замечено
>
> Вы можете найти больше в [docs](/v3/documentation/smart-contracts/message-management/sending-messages). Также вы можете прыгнуть в [layout](/v3/documentation/smart-contracts/message-management/sending-messages#message-layout) с этой ссылкой.

> 💡 Полезные ссылки
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["store_uint()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> ["store_slice()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> ["store_coins()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_coins)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#end_cell)
>
> ["send_raw_message()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### Как поместить тело как ссылку на внутреннюю ячейку сообщения

В теле сообщения, которое следует за флагами и другими техническими данными, мы можем отправлять `int`, `slice` и `cell`. В последнем случае необходимо установить бит на `1` перед `store_ref()`, чтобы указать, что `cell` будет продолжаться.

Мы также можем отправить текст сообщения внутри «ячейки», если мы уверены, что у нас достаточно места. В этом случае нам нужно установить бит на «0».

```func
;; Мы используем литерал `a`, чтобы получить действительный адрес внутри строки, содержащей адрес 
добавление маски = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
ячейка message_body = begin_cell() ;; Создание ячейки с сообщением
    . tore_uint(op, 32)
    .store_slice("❤️")
. nd_cell();
    
ячейка msg = begin_cell()
    . tore_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(1, 1) ;; установите бит 1, чтобы указать, что ген будет идти
    .store_ref(message_body)
. nd_cell();

send_raw_message(msg, 3); ;; режим 3 - оплата сборов отдельно и игнорирование ошибок 
```

> 💡 Замечено
>
> В этом примере мы используем букву `a` для получения адреса. Вы можете найти больше о строковых буквах в [docs](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)

> 💡 Замечено
>
> В этом примере мы использовали третий способ для взятия входящих тонн и отправки точно столько же, сколько указано (сумма), при оплате комиссии с баланса контракта и игнорировании ошибок. Для возврата всех полученных тонн, вычитание комиссии, а режим 128 посылает весь баланс.

> 💡 Замечено
>
> Мы [создаем сообщение](/v3/documentation/smart-contracts/func/cookbook#how-to-build-an-internal-message-cell), но добавляем тело сообщения отдельно.

> 💡 Полезные ссылки
>
> ["begin_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> ["store_uint()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> ["store_slice()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> ["store_coins()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#store_coins)
>
> ["end_cell()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#end_cell)
>
> ["send_raw_message()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### Как содержать тело как кусочек внутренней ячейки сообщения

При отправке сообщений сообщение может быть отправлено либо как «ячейку», либо как «кусок». В этом примере мы отправляем текст сообщения внутри ломтика.

```func
;; Мы используем литерал `a`, чтобы получить действительный адрес внутри строки, содержащей адрес 
добавление маски = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
фрагмент message_body = "❤️"; 

клеток msg = begin_cell()
    . tore_uint(0x18, 6)
    . tore_slice(addr)
    .store_coins(amount)
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(op, 32)
    .store_slice(message_body)
.end_cell();

send_raw_message(msg, 3); ;; режим 3 - Оплата сборов отдельно и игнорирование ошибок 
```

> 💡 Замечено
>
> В этом примере мы используем букву `a` для получения адреса. Вы можете найти больше о строковых буквах в [docs](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)

> 💡 Замечено
>
> В этом примере мы использовали третий способ для взятия входящих тонн и отправки точно столько же, сколько указано (сумма), при оплате комиссии с баланса контракта и игнорировании ошибок. Для возврата всех полученных тонн, вычитание комиссии, а режим 128 посылает весь баланс.

> 💡 Замечено
>
> Мы [создаем сообщение](/v3/documentation/smart-contracts/func/cookbook#how-to-build-an-internal-message-cell), но добавляем сообщение в виде лицензии.

### Как повторить трубки (в обоих направлениях)

Если мы хотим работать с массивом или стеком в FunC, то трубка будет необходима. И прежде всего нам нужно иметь возможность итерации ценностей для работы с ними.

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

() main () {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    int len = t. len();
    
    int i = 0;
    while (i < len) {
        int x = t. t(i);
        ;; сделать что-то с x
        i = i + 1;
    }

    i = len - 1;
    while (i >= 0) {
        int x = t. t(i);
        ;; сделать что-то с x
        i = i - 1;
    }
}
```

> 💡 Замечено
>
> Мы объявляем функцию сборки `tlen`. You can read more [here](/v3/documentation/smart-contracts/func/docs/functions#assembler-function-body-definition) and see [list of all assembler commands](/v3/documentation/tvm/instructions).
>
> Также мы определяем функцию `to_tuple`. Он просто изменяет тип данных любого ввода, так что будьте осторожны при его использовании.

### Как писать собственные функции, используя ключевое слово `asm`

При использовании любых функций мы используем заранее подготовленные методы внутри `stdlib.fc`. Но на самом деле у нас есть еще много возможностей, доступных нам, и нам нужно научиться писать их сами.

Например, мы имеем метод `tpush`, который добавляет элемент в "tuple", но без `tpop`. В этом случае мы должны сделать это:

```func
;; ~ означает, что он модифицирует метод
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP"; 
```

Если мы хотим знать длину `tuple` для итерации, то нам следует написать новую функцию с инструкцией 'TLEN':

```func
int tuple_length (tuple t) asm "TLEN";
```

Некоторые примеры функций, уже известных нам из stdlib.fc:

```func
срез begin_parse(ячейка c) asm "CTOS";
builder begin_cell() asm "NEWC";
клеток end_cell(builder b) asm "ENDC";
```

> 💡 Полезные ссылки:
>
> ["Изменение метода" в документах](/v3/documentation/smart-contracts/func/docs/statements#modifying-methods)
>
> ["stdlib" в документах](/v3/documentation/smart-contracts/func/docs/stdlib)
>
> ["Инструкции TVM" в документах](/v3/documentation/tvm/instructions)

### Итерация n-nested канальцев

Иногда мы хотим повторить вложенные трубки. Следующий пример будет повторяться и печатать все элементы в канале `[[2,6],[1,[3,[3,5]]], 3]` начиная с головы

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> (tuple) to_tuple (X x) asm "NOP";

;; определение глобальной переменной
глобальной int max_value;

() iterate_tuple (tuple t) impure {
    repeat (t. uple_length()) {
        var value = t~tpop();
        if (is_tuple(value)) {
            tuple tuple_value = cast_to_tuple(value);
            iterate_tuple(tuple_value);
        }
        else {
            if(value > max_value) {
                max_value = value;
            }
        }
    }
}

() main () {
    tuple t = to_tuple([[2, ], [1, [3, [3, 5]], 3]);
    int len = t. uple_length();
    max_value = 0; ;; сброс max_value;
    iterate_tuple(t); ;; итерация трубки и найти максимальное значение
    ~dump(max_value); ;; 6
}
```

> 💡 Полезные ссылки
>
> ["Глобальные переменные" в документах](/v3/documentation/smart-contracts/func/docs/global_variables)
>
> ["~dump" в документах](/v3/documentation/smart-contracts/func/docs/builtins#dump-variable)
>
> ["Инструкции TVM" в документах](/v3/documentation/tvm/instructions)

### Основные операции с канавками

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

() {
    ;; создание пустой трубки
    трубных имен = empty_tuple(); 
    
    ;; push новых элементов
    имена~tpush("Naito Narihira");
    names~tpush("Шираки Синчихи");
    names~tpush("Akamatsu Hachemon");
    names~tpush("Такаки Юичихи");
    
    ;; поп последнего предмета
    маски last_name = names~tpop();

    ;; получить первый элемент
    маски первого _name = имена. irst();

    ;; получить предмет по индексу
    срез best_name = имена. t(2);

    ;; получение длины списка 
    int number_names = names.tlen();
}
```

### Разрешение типа X

В следующем примере проверяется, содержится ли какое-то значение в палочке, но в туале содержатся значения X (ячейка, кусок, дюйм, int). Нам нужно проверить значение и применить соответственно.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cast_to_cell (X x) asm "NOP";
forall X -> slice cast_to_slice (X x) asm "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

forall X -> () resolve_type (X value) impure {
    ;; значение здесь типа X, поскольку мы не знаем, что такое точное значение - нам нужно проверить значение и затем нанести его
    
    if (is_null(value)) {
        ;; сделать что-то с null
    }
    elseif (is_int(value)) {
        int valueAsInt = cast_to_int(value);
        ;; сделать что-то с int
    }
    elseif (is_slice(value)) {
        slice valueAsSlice = cast_to_slice(value);
        ; сделать что-то с сликом
    }
    elseif (is_cell(value)) {
        cell valueAsCell = cast_to_cell(value);
        ; сделать что-то с ячейкой
    }
    elseif (is_tuple(value)) {
        tuple valueAsTuple = cast_to_tuple(value);
        ;; сделать что-то с туз
    }
}

() main () {
    ; создание пустой трубки
    тузовой стек = empty_tuple();
    ;; давайте скажем, что у нас есть трубка и не знаем точные типы их
    stack~tpush("Некоторые текст");
    стека~tpush(4);
    ; мы используем var, потому что мы не знаем тип значения
    var value = stack~tpop();
    resolve_type(value);
}
```

> 💡 Полезные ссылки
>
> ["Инструкции TVM" в документах](/v3/documentation/tvm/instructions)

### Как получить текущее время

```func
int current_time = now();
  
if (current_time > 1672080143) {
    ;; do some stuff 
}
```

### Как сгенерировать случайное число

:::caution черновик
Обратите внимание, что этот метод генерации случайных чисел небезопасен.

Ознакомьтесь с [генерацией случайных чисел](/v3/guidelines/smart-contracts/security/random-number-generation) для получения дополнительной информации.
:::

```func
randomize_lt(); ;; сделать это один раз

int a = rand(10);
int b = rand(1000000);
int c = random();
```

### Операции модулей

В качестве примера скажем, что мы хотим выполнить следующий расчет всех 256 чисел : `(xp + zp)*(xp-zp)`. Поскольку большинство этих операций используются для криптографии, в следующем примере мы используем оператор модулей для montogomery кривых.
Обратите внимание, что xp+zp является допустимым именем переменной ( без пробелов между ).

```func
(int) modulo_operations (int xp, int zp) {  
   ;; 2^255 - 19 является простым числом для кривых монтгомерей, что означает, что все операции должны проводиться против своего основного
   int prime = 5789604461865809771178549250434395392663499233282028197287920039564819949; 

   ;; muldivmod обрабатывает следующие две линии самого
   ; int xp+zp = (xp + zp) % prime;
   ;; int xp-zp = (xp - zp + prime) % prime;
   (_, int xp+zp*xp-zp) = muldivmod(xp + zp, xp - zp, prime);
   return xp+zp*xp-zp;
}
```

> 💡 Полезные ссылки
>
> ["muldivmod" в документах](/v3/documentation/tvm/instructions#A98C)

### Как бросить ошибки

```func
число int = 198;

throw_if(35, число > 50); ;; ошибка будет вызвана только если число больше 50

throw_unless(39, number == 198); ;; ошибка будет срабатывать только если число НЕ EQUAL до 198

броска (36); ;; ошибка все равно будет вызвана
```

[Стандартные коды исключений tvm](/v3/documentation/tvm/tvm-exit-codes)

### Обращение трубки

Потому что паук хранит данные в виде стека, иногда мы должны обратить тупик, чтобы читать данные с другого конца.

```func
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

(tuple) reverse_tuple (tuple t1) {
    tuple t2 = empty_tuple();
    repeat (t1. uple_length()) {
        var value = t1~tpop();
        t2~tpush(value);
    }
    return t2;
}

() main {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    трубка обратно_t = reverse_tuple(t);
    ~dump(reversed_t); ;; [10 9 8 7 6 4 3 2 1]
}
```

> 💡 Полезные ссылки
>
> ["tpush()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#tpush)

### Как удалить элемент с определенным индексом из списка

```func
int tlen (tuple t) asm "TLEN";

(tuple, ()) remove_item (tuple old_tuple, int place) {
    tuple new_tuple = empty_tuple();

    int i = 0;
    в то время (i < old_tuple. len()) {
        int el = old_tuple. t(i);
        если (i ! place) {
            new_tuple~tpush(el);
        }
        i += 1;  
    }
    return (new_tuple, ());
}

() main () {
    tuple numbers = empty_tuple();

    numbers~tpush(19);
    numbers~tpush(999);
    numbers~tpush(54);

    ~dump(numbers); ;; [19 999 54]

    numbers~remove_item(1); 

    ~dump(numbers); ;; [19 54]
}
```

### Определить, если кусочки равны

Существует два различных способа определения равенства. Один из них основан на хэше спрайтов, а другой - с помощью инструкции asm SDEQ.

```func
int are_slices_equal_1? (slice a, slice b) {
    return a.slice_hash() == b. lice_hash();
}

int are_slices_equal_2? (slice a, slice b) asm "SDEQ";

() main () {
    slice a = "Некоторый текст";
    Кусочек b = "Некоторый текст";
    ~dump(are_slices_equal_1? a, b)); ;; -1 = true

    a = "Текст";
    ;; Мы используем буквенный `a` чтобы получить действительный адрес внутри строки, содержащей адрес
    b = "EQDKbjIcfM6ezt8KJLshZJJSqX7XOA4ff-W72r5gqPrHF"a;
    ~dump(are_slices_equal_2? a, b)); ;; 0 = false
}
```

#### 💡 Полезные ссылки

- ["slice_hash()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_hash)
- ["SDEQ" в документах](/v3/documentation/tvm/instructions#C705)

### Определяет, совпадают ли ячейки

Мы можем легко определить равенство клеток на основе их хэша.

```func
int are_cells_equal? (cell a, cell b) {
    return a.cell_hash() == b. ell_hash();
}

() {
    ячейка = begin_cell()
            . tore_uint(123, 16)
            . nd_cell();

    ячейка b = begin_cell()
            . tore_uint(123, 16)
            . nd_cell();

    ~dump(are_cells_equal?(a, b)); ;; -1 = true
}
```

> 💡 Полезные ссылки
>
> ["cell_hash()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)

### Определить, если трубки равны

Более продвинутым примером является итерация и сравнение каждого из значений трубочки. Так как они являются X необходимо проверить и применить к соответствующему типу и если трубка для повторной рекурсии.

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cell cast_to_cell (X x) asm "NOP";
forall X -> срез cast_to_slice (X x) срез "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
int are_slices_equal? (slice a, slice b) asm "SDEQ";

int are_cells_equal? (cell a, cell b) {
    return a. ell_hash() == b. ell_hash();
}

(int) are_tuples_equal? (tuple t1, tuple t2) {
    int equal? = -1; ;; начальное значение для true
    
    если (t1. uple_length() != t2. uple_length()) {
        ;; если трубки отличаются длиной, они не могут быть равны
        возврату 0;
    }

    int i = t1. uple_length();
    
    while (i > 0 & equal? {
        v1 = t1~tpop();
        var v2 = t2~tpop();
        
        if (is_null(t1) & is_null(t2)) {
            ; nulls всегда равны
        }
        elseif (is_int(v1) & is_int(v2)) {
            if (cast_to_int(v1) ! cast_to_int(v2)) {
                равны? = 0;
            }
        }
        elseif (is_slice(v1) & is_slice(v2)) {
            if (~ are_slices_equal? cast_to_slice(v1), cast_to_slice(v2))) {
                equal? = 0;
            }
        }
        elseif (is_cell(v1) & is_cell(v2)) {
            if (~ are_cells_equal? cast_to_cell(v1), cast_to_cell(v2))) {
                equal? = 0;
            }
        }
        elseif (is_tuple(v1) & is_tuple(v2)) {
            ; рекурсивно определяют вложенные трубки
            если (~ are_tuples_equal? cast_to_tuple(v1), cast_to_tuple(v2))) {
                equal? = 0;
            }
        }
        else {
            равно? = 0;
        }

        i -= 1;
    }

    возврат равны?
}

() main () {
    tuple t1 = cast_to_tuple([[2, 6], [1, [3, 5]]], 3]);
    tuple t2 = cast_to_tuple([[2, 6], [1, [3, [3, 5]]], 3]);

    ~dump(are_tuples_equal? t1, t2)); ;; -1 
}
```

> 💡 Полезные ссылки
>
> ["cell_hash()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)
>
> ["Инструкции TVM" в документах](/v3/documentation/tvm/instructions)

### Генерировать внутренний адрес

Нам нужно генерировать внутренний адрес, когда наш контракт должен разместить новый контракт, но не знаю его адреса. Предположим, у нас уже есть `state_init` - код и данные нового контракта.

Создает внутренний адрес для соответствующего MsgAddressInt TLB.

```func
(slice) generate_internal_address (int workchain_id, cell state_init) {
    ;; addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;

    return begin_cell()
        .store_uint(2, 2) ;; addr_std$10
        .store_uint(0, 1) ;; anycast nothing
        .store_int(workchain_id, 8) ;; workchain_id: -1
        .store_uint(cell_hash(state_init), 256)
    .end_cell().begin_parse();
}

() main () {
    slice deploy_address = generate_internal_address(workchain(), state_init);
    ;; then we can deploy new contract
}
```

> 💡 Замечено
>
> В этом примере мы используем «workchain()», чтобы получить id рабочей цепочки. Подробнее о Workchain ID можно найти в [docs](/v3/documentation/smart-contracts/addresses#workchain-id).

> 💡 Полезные ссылки
>
> ["cell_hash()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)

### Генерировать внешний адрес

Мы используем схему TL-B от [block.tlb](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L101C1-L101C12) для понимания того, как нам нужно создать адрес в этом формате.

```func
(int) ubitsize (int a) asm "UBITSIZE";

slice generate_external_address (int address) {
    ;; addr_extern$01 len:(## 9) external_address:(bits len) = MsgAddressExt;
    
    int address_length = ubitsize(address);
    
    возвращает begin_cell()
        . tore_uint(1, 2) ;; addr_extern$01
        .store_uint(address_length, 9)
        . tore_uint(адрес, address_length)
    .end_cell().begin_parse();
}
```

Поскольку нам нужно определить количество битов, занятых адресом, также необходимо [объявить функцию asm](#how-to-write-own-functions-using-asm-keyword) с помощью опкода `UBITSIZE`, , которая возвращает минимальное количество бит, необходимое для хранения этого номера.

> 💡 Полезные ссылки
>
> ["Инструкции TVM" в документах](/v3/documentation/tvm/instructions#B603)

### Как хранить и загружать словарь в локальном хранилище

Логика для загрузки словаря

```func
slice local_storage = get_data().begin_parse();
ячейка dictionary_cell = new_dict();
if (~ slice_empty?(local_storage)) {
    dictionary_cell = local_storage~load_dict();
}
```

Логика хранения словаря похожа на следующий пример:

```func
set_data(begin_cell().store_dict(dictionary_cell).end_cell());
```

> 💡 Полезные ссылки
>
> ["get_data()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#get_data)
>
> ["new_dict()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#new_dict)
>
> ["slice_empty?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_empty)
>
> ["load_dict()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#load_dict)
>
> ["~" в документах](/v3/documentation/smart-contracts/func/docs/statements#unary-operators)

### Как отправить простое сообщение

Обычный для нас способ отправить тонны с комментарием – это простое сообщение. Чтобы уточнить, что тело сообщения является «комментарием», необходимо установить «32 бита» перед текстом сообщения в 0.

```func
ячейка msg = begin_cell()
    .store_uint(0x18, 6) ;; флаги
    . tore_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; адрес назначения
    .store_coins(100) ;; количество нанотонов для отправки
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(0, 32) ;; ноль opcode - означает простой перевод сообщения с комментарием
    . tore_slice("Привет от FunC!") ;; комментарий
.end_cell();
send_raw_message(msg, 3); ;; режим 3 - оплата сборов отдельно, игнорирование ошибок
```

> 💡 Полезные ссылки
>
> ["Макет сообщений" в документах](/v3/documentation/smart-contracts/message-management/sending-messages)

### Как отправить сообщение с входящим аккаунтом

Приведенный ниже пример полезен для нас, если нам нужно выполнить любые действия между пользователем и основным договором, то есть, нам нужен контракт с прокси сервером.

```func
() recv_internal (slice in_msg_body) {
    {-
        This is a simple example of a proxy-contract.
        It will expect in_msg_body to contain message mode, body and destination address to be sent to.
    -}

    int mode = in_msg_body~load_uint(8); ;; first byte will contain msg mode
    slice addr = in_msg_body~load_msg_addr(); ;; then we parse the destination address
    slice body = in_msg_body; ;; everything that is left in in_msg_body will be our new message's body

    cell msg = begin_cell()
        .store_uint(0x18, 6)
        .store_slice(addr)
        .store_coins(100) ;; just for example
        .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
        .store_slice(body)
    .end_cell();
    send_raw_message(msg, mode);
}
```

> 💡 Полезные ссылки
>
> ["Макет сообщений" в документах](/v3/documentation/smart-contracts/message-management/sending-messages)
>
> ["load_msg_addr()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#load_msg_addr)

### Как отправить сообщение со всем балансом

Если нам нужно отправить весь баланс смарт-контракта, то в этом случае мы должны использовать отправку `mode 128`. Примером такого случая может служить контракт с прокси, который принимает платежи и направляет на рассмотрение основного контракта.

```func
ячейка msg = begin_cell()
    .store_uint(0x18, 6) ;; флаги
    . tore_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; адрес назначения
    . tore_coins(0) ;; сейчас мы не заботимся об этом значении
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(0, 32) ;; ноль opcode - означает простой перевод сообщения с комментарием
    .store_slice("Привет от FunC!") ;; комментарий
. nd_cell();
send_raw_message(msg, 128); ;; режим = 128 используется для сообщений, которые несут все оставшиеся остатки баланса текущего смарт-контракта
```

> 💡 Полезные ссылки
>
> ["Макет сообщений" в документах](/v3/documentation/smart-contracts/message-management/sending-messages)
>
> ["Режим сообщения" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### Как отправить сообщение с длинным текстовым комментарием

Как мы знаем, только 127 символов могут помещаться в одну «ячейку» (< 1023 бит). В случае, если нам нужно больше - нам нужно организовать змеи клетки.

```func
{-
    Если мы хотим отправить сообщение с очень большим комментарием, мы должны разделить комментарий на несколько кусочков.
    Каждая часть должна иметь <1023 бит данных (127 знаков).
    Каждый кусочек должен иметь ссылку на следующую структуру, образующую похожую на змею.
-}

клеток = begin_cell()
    . tore_uint(0, 32) ;; ноль opcode - простое сообщение с комментарием
    . tore_slice("длинное сообщение...")
    .store_ref(begin_cell()
        . tore_slice(" вы можете сохранить строку почти любой длины здесь. )
        .store_ref(begin_cell()
            . tore_slice(" просто не забывайте о лимите 127 символов для каждого ломтика")
        . nd_cell())
    .end_cell())
.end_cell();

ячейки msg = begin_cell()
    . tore_uint(0x18, 6) ;; флаги
    ;; Мы используем букву `a`, чтобы получить действительный адрес внутри строки с адресом 
    . tore_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; адрес назначения
    . tore_coins(100) ;; количество нанотонов для отправки
    . tore_uint(0, 1 + 4 + 4 + 64 + 32 + 1) ;; заголовки сообщений (см. страницу отправки сообщений)
    . tore_uint(1, 1) ;; мы хотим сохранить тело в виде ref
    .store_ref(body)
. nd_cell();
send_raw_message(msg, 3); ;; режим 3 - отдельная оплата сборов, игнорирование ошибок
```

> 💡 Полезные ссылки
>
> ["Внутренние сообщения" в документах](/v3/documentation/smart-contracts/message-management/internal-messages)

### Как получить только данные из кусочка (без рефералов)

Если мы не заинтересованы в `refs` внутри `slice`, то мы можем получить отдельную дату и работать с ней.

```func
slice s = begin_cell()
    .store_slice("Некоторые биты данных...")
    .store_ref(begin_cell().end_cell()) ;; некоторые ссылки
    .store_ref(begin_cell().end_cell()) ;; некоторые ссылки
.end_cell().begin_parse();

slice s_only_data = s.preload_bits(s.slice_bits());
```

> 💡 Полезные ссылки
>
> ["Примитивы массы" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice-primitives)
>
> ["preload_bits()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#preload_bits)
>
> ["slice_bits()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_bits)

### Как определить свой собственный метод изменения

Изменение методов позволяет изменять данные в пределах одной и той же переменной. Это можно сравнить с ссылками на другие языки программирования.

```func
(slice, (int)) load_digit (slice s) {
    int x = s~load_uint(8); ;; загрузить 8 бит (один символ) из маски
    x = 48; ;; символ '0' имеет код 48, так что мы вычитаем цифру в виде возвращаемой переменной
    (s, (x)); ;; return our modified slice and loaded digit
}

() main () {
    slice s = "258";
    int c1 = s~load_digit();
    int c2 = s~load_digit();
    int c3 = s~load_digit();
    ;; здесь s равен "", а c1 = 2, c2 = 5, c3 = 8
}
```

> 💡 Полезные ссылки
>
> ["Изменение методов" в документах](/v3/documentation/smart-contracts/func/docs/statements#modifying-methods)

### Как поднять число до силы n

```func
;; Неоптимизированный вариант
int pow (int a, int n) {
    int i = 0;
    int value = a;
    в то время как (i < n - 1) {
        a *= value;
        i + = 1;
    }
    возвращение a;
}

;; Оптимизированный вариант
(int) binpow (int n, int e) {
    if (e == 0) {
        return 1;
    }
    if (e == 1) {
        return n;
    }
    int p = binpow(n, e / 2);
    p *= p;
    if (e % 2) == 1) {
        p *= n;
    }
    return p;
}

() {
    int num = binpow(2, 3);
    ~dump(num); ;; 8
}
```

### Как преобразовать строку в подсказку

```func
срез string_number = "26052021";
int number = 0;

пока (~ string_number. lice_empty )) {
    int char = string_number~load_uint(8);
    number = (number * 10) + (char - 48); ;; Мы используем таблицу ASCII
}

~дам(число);
```

### Как преобразовать подсказку в строку

```func
int n = 261119911;
builder string = begin_cell();
tuple chars = null();
do {
    int r = n~divmod(10);
    chars = cons(r + 48, chars);
} до (n == 0);
do {
    int char = chars~list_next();
    string~store_uint(char, 8);
} до (пуст? chars));

результат маски = строка. nd_cell().begin_parse();
~dump(result);
```

### Как итерация словарей

Словарь очень полезен при работе с большим количеством данных. Мы можем получить минимальные и максимальные значения клавиш, используя встроенные методы `dict_get_min?` и `dict_get_max?` соответственно. Кроме того, мы можем использовать `dict_get_next?` для итерации словаря.

```func
ячейка d = new_dict();
d~udict_set(256, 1, "value 1");
d~udict_set(256, 5, "value 2");
d~udict_set(256, 12, "value 3");

;; итерация ключей от маленького до большого
(int key, slice val, int flag) = d. dict_get_min? 256);
while (flag) {
    ;; сделать что-то с ключ->val
    
    (ключ, val, flag) = d. dict_get_next?(256, ключ);
}
```

> 💡 Полезные ссылки
>
> ["Словари примитивов" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dictionaries-primitives)
>
> ["dict_get_max?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_max)
>
> ["dict_get_min?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_min)
>
> ["dict_get_next?()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_next)
>
> ["dict_set()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_set)

### Как удалить значение из словарей

```func
имена ячеек = new_dict();
names~udict_set(256, 27, "Alice");
names~udict_set(256, 25, "Bob");

names~udict_delete?(256, 27);

(slice val, int key) = имена. dict_get?(256, 27);
~dump(val); ;; null() -> означает, что ключ не найден в словаре
```

### Рекурсивно итерация ячеек

Как мы знаем, один `cell` может хранить до `1023 bits` данных и до `4 refs`. Чтобы обойти этот лимит, мы можем использовать дерево клеток, но для этого нам нужно иметь возможность повторить его для правильной обработки данных.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() {
    ;; просто какая-то ячейка, например
    ячейка c = begin_cell()
        . tore_uint(1, 16)
        . tore_ref(begin_cell()
            . tore_uint(2, 16)
        .end_cell())
        . tore_ref(begin_cell()
            . tore_uint(3, 16)
            . tore_ref(begin_cell()
                . tore_uint(4, 16)
            . nd_cell())
            . tore_ref(begin_cell()
                . tore_uint(5, 16)
            . nd_cell())
        . nd_cell())
    . nd_cell();

    ;; создание трубки без данных, которая играет роль стека
    трубки = null();
    ;; довести главную ячейку в стек, чтобы обработать ее в цикле
    stack~push_back(c);
    ;; делайте это, пока стек не нулевый
    пока (~ стек. s_null()) {
        ;; получить ячейку из стека и преобразовать ее в кусочек, чтобы иметь возможность обработать ее в
        кусочков = stack~pop_back(). egin_parse();

        ;; сделать что-то с данными

        ;; если текущий кусочек имеет ответ, добавьте его в стек
        повторов (s. lice_refs()) {
            stack~push_back(s~load_ref());
        }
    }
}
```

> 💡 Полезные ссылки
>
> ["Lisp-style lists" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#lisp-style-lists)
>
> ["null()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#null)
>
> ["slice_refs()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_refs)

### Как переписать через список стилей lisp

Тип данных может удерживать до 255 значений. Если этого недостаточно, то мы должны использовать список стилей lisp-. Мы можем поместить трубку в трубку, тем самым обойдя границу.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() main () {
    ;; some example list
    tuple l = null();
    l~push_back(1);
    l~push_back(2);
    l~push_back(3);

    ;; iterating through elements
    ;; note that this iteration is in reversed order
    while (~ l.is_null()) {
        var x = l~pop_back();

        ;; do something with x
    }
}
```

> 💡 Полезные ссылки
>
> ["Lisp-style lists" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#lisp-style-lists)
>
> ["null()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib/#null)

### Как отправить развёрнутое сообщение (только для stateInit, с stateInit и тело)

```func
() deploy_with_stateinit(cell message_header, cell state_init) impure {
  var msg = begin_cell()
    . tore_slice(begin_parse(msg_header))
    tore_uint(2 + 1, 2) ;; init:(Maybe (либо StateInit ^StateInit))
    . tore_uint(0, 1) ;; body:(либо X ^X)
    . tore_ref(state_init)
    . nd_cell();

  ;; mode 64 - перенос оставшегося значения в новом сообщении
  send_raw_message(msg, 64); 
}

() deploy_with_stateinit_body(cell message_header, cell state_init, combody) impure {
  var msg = begin_cell()
    . tore_slice(begin_parse(msg_header))
    .store_uint(2 + 1, 2) ;; init:(Maybe (Either StateInit ^StateInit))
    . tore_uint(1, 1) ;; тел:(либо X ^X)
    . tore_ref(state_init)
    .store_ref(body)
    . nd_cell();

  ;; mode 64 - переноси оставшееся значение в новом сообщении
  send_raw_message(msg, 64); 
}
```

### Как создать ячейку stateInit

```func
() build_stateinit(cell init_code, cell init_data) {
  var state_init = begin_cell()
    . tore_uint(0, 1) ;; split_depth:(Maybe (## 5))
    .store_uint(0, 1) ;; special:(Maybe TickTock)
    . tore_uint(1, 1) ;; (Maybe ^Cell)
    .store_uint(1, 1) ;; (Maybe ^Cell)
    . tore_uint(0, 1) ;; (HashmapE 256 SimpleLib)
    . tore_ref(init_code)
    .store_ref(init_data)
    .end_cell();
}
```

### Как рассчитать адрес контракта (используя stateInit)

```func
() calc_address(cell state_init) {
  var future_address = begin_cell() 
    . tore_uint(2, 2) ;; addr_std$10
    .store_uint(0, 1) ;; в любом случае:(Maybe Anycast)
    . tore_uint(0, 8) ;; workchain_id:int8
    .store_uint(cell_hash(state_init), 256) ;; address:bits256
    .end_cell();
}
```

### Как обновить логику смарт-контракта

Ниже представлен простой смарт-контракт `СounterV1`, который обладает функциональностью для увеличения счетчика и обновления логики смарт-контракта.

```func
() recv_internal (slice in_msg_body) {
    int op = in_msg_body~load_uint(32);
    
    if (op == op::increase) {
        int increase_by = in_msg_body~load_uint(32);
        ctx_count+= increase_by;
        save_data();
        return ();
    }

    if (op == op::upgrade) {
        код ячейки = in_msg_body~load_ref();
        set_code(код);
        возвращение ();
    }
}
```

После работы с смарт-контрактом, вы понимаете, что вы не имеете возможности уменьшить счетчик. Вы должны скопировать код smart-contract `CounterV1` и рядом с функцией `increase`, добавить новую функцию `decrease`. Теперь ваш код выглядит следующим образом:

```func
() recv_internal (slice in_msg_body) {
    int op = in_msg_body~load_uint(32);
    
    if (op == op::increase) {
        int increase_by = in_msg_body~load_uint(32);
        ctx_count+= increase_by;
        save_data();
        return ();
    }

    if (op == op::decrease) {
        int decrease_by = in_msg_body~load_uint(32);
        ctx_coun-= increase_by;
        save_data();
        return ();
    }

    if (op == op::upgrade) {
        код ячейки = in_msg_body~load_ref();
        set_code(код);
        возвращение ();
    }
}
```

Как только умный контракт `CounterV2` будет готов, вы должны скомпилировать его в `cell` и отправить сообщение об обновлении в `CounterV1` smart-contract.

```javascript
await contractV1.sendUpgrade(provider.sender(), {
    code: await compile('ContractV2'),
    значение: toNano('0.05'),
});
```

> 💡 Полезные ссылки
>
> [Возможно ли перерасположить код на существующий адрес или же он должен быть развернут как новый контракт?](/v3/documentation/faq#is-it-possible-to-re-deploy-code-to-an-existing-address-or-does-it-have-to-be-deployed-as-a-new-contract)
>
> ["set_code()" в документах](/v3/documentation/smart-contracts/func/docs/stdlib#set_code)
