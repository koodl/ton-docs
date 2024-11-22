# RLDP

Осуществление:

- https://github.com/ton-blockchain/ton/tree/master/rldp
- https://github.com/ton-blockchain/ton/tree/master/rldp2
- https://github.com/ton-blockchain/ton/tree/master/rldp-http-proxy

## Общий обзор

RLDP - надежный большой протокол датаграмм - это протокол, который запускается поверх ADNL UDP, , который используется для передачи больших блоков данных, и
включает алгоритмы коррекции Forward Error Correction (FEC) в качестве замены принятых пакетов на другой стороне.
Это позволяет передавать данные между сетевыми компонентами более эффективно, но с большим потреблением трафика.

RLDP используется везде в инфраструктуре TON, например, для загрузки блоков с других узлов и передачи им данных,
для доступа к сайтам TON и TON Storage.

## Protocol

RLDP использует для связи следующие TL структуры:

```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;
fec.roundRobin data_size:int symbol_size:int symbols_count:int = fec.Type;
fec. nline data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
rldp. onfirm transfer_id:int256 part:int seqno:int = rldp.MessagePart;
rldp.complete transfer_id:int256 part:int = rldp.MessagePart;

rldp.message id:int256 data:bytes = rldp. essage;
rldp.query query_id:int256 max_answer_size:long timeout:int data:bytes = rldp.Message;
rldp.answer query_id:int256 data:bytes = rldp.Message;
```

Сериализованная структура завернута в схему `adnl.message.custom` TL и отправлена по ADNL UDP.
RLDP Transfers используются для передачи больших данных, генерируется случайный `transfer_id` и сами данные обрабатываются алгоритмом FEC.
Полученные части завернуты в структуру `rldp.messagePart` и отправляются пиру до тех пор, пока пир не отправит нам `rldp.complete` или до истечения времени.

Когда получатель собрал фрагменты `rldp. essagePart` необходим для сборки полного сообщения, он скомбинирует их вместе, декодирует использование FEC и
десериализирует результирующий массив байтов в один из `rldp. Структуры uery` или `rldp.answer` в зависимости от типа (ID префикса tl).

### FEC

Валидные алгоритмы коррекции Forward Error для использования в RLDP являются RoundRobin, Online и RaptorQ.
Currently for data encoding [RaptorQ](https://www.qualcomm.com/media/documents/files/raptorq-technical-overview.pdf) is used.

#### Раптор

Суть РапторQ заключается в том, что данные разделены на так называемые символы - блоки того же и предопределенного размера.

Матрицы создаются из блоков, и к ним применяются дискретные математические операции. Это позволяет нам создать почти бесконечное количество символов.
из тех же данных. Все символы смешиваются, и можно восстановить потерянные пакеты без запроса дополнительных данных с сервера, в то время как использование пакетов меньше, чем если бы мы отправили те те же части в цикле.

Созданные символы отправляются пиру до тех пор, пока не сообщит, что все данные были получены и восстановлены (декодированы), применяя одни и те же дискретные операции.

[[Пример реализации RaptorQ на Голанге]](https://github.com/xssnick/tonutils-go/tree/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq)

## RLDP-HTTP

Для взаимодействия с сайтами TON используется HTTP, завернутый в RLDP. Хост запускает свой сайт на любом HTTP веб-сервере и запускает рядом с ним rldp-http-http-proxy.
Все запросы от сети TON поступают по протоколу RLDP на прокси, и прокси перекомпилирует запрос в простой HTTP и вызывает оригинальный веб-сервер локально.

Пользователь со своей стороны запускает прокси, например, [Tonutils Proxy](https://github.com/xssnick/TonUtils-Proxy) и использует \`. весь трафик завершается в обратном порядке, запросы переходят на локальный HTTP-прокси, и он отправляет их через RLDP на удаленный сайт TON.

HTTP внутри RLDP реализован с использованием структур TL:

```tlb
http.header name:string value:string = http.Header;
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
http.response http_version:string status_code:int reason:string headers:(vector http. eader) no_payload:Bool = http.Response;

http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

Это не просто HTTP в текстовой форме, все упаковано в двоичный TL и распаковано для отправки на веб-сервер или браузер самим прокси.

Ниже приводится схема работы:

- Клиент отправляет `http.request`
- Сервер проверяет заголовок `Content-Length` при получении запроса
- - Если не 0, отправляет запрос `http.getNextPayloadPart` клиенту
- - При получении запроса клиент отправляет `http.payloadPart` - запрошенную часть тела в зависимости от `seqno` и `max_chunk_size`.
- - Сервер повторяет запросы, увеличивая `seqno`, пока он не получит все чанки от клиента, i. . до тех пор, пока поле `last:Bool` последнего полученного чанка не верно.
- После обработки запроса сервер отправляет `http.response`, клиент проверяет заголовок `Content-Length`
- - Если это не 0, то посылает `http. etNextPayloadPart` запрос на сервер, и операции повторяются, как в случае с клиентом, но наоборот.

## Запросить сайт TON

Чтобы понять, как работает RLDP, давайте рассмотрим пример получения данных с сайта TON `foundation.ton`.
Допустим, у нас уже есть ADNL адрес, вызвав метод контракта с NFT-DNS, [определил адрес и порт службы RLDP с помощью DHT](https://github. om/xssnick/ton-deep-doc/blob/master/DHT.md), и [подключен к нему](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-UDP-Internal.md).

### Отправить GET запрос на `foundation.ton`

Для этого заполните структуру:

```tlb
http.request id:int256 метод:string url:string http_version:string заголовки:(vector http.header) = http.Response;
```

Заполните поля для заселения `http.request`:

```
e191b161 -- TL ID http. equest      
116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245de471194 -- id = {random}
03 474554 -- метод = string `GET`
16 687474703a2f2f666f756e646174696f6e2e746f6e2f6e2f 00 -- url = строка `http://foundation. on/`
08 485454502f312e31 000000 -- http_version = string `HTTP/1. `
01000000 -- заголовки (1)
   04 486f7374 000000 -- name = Host
   0e 666f756e646174696f6e2e746f6e 00 -- значение = foundation.ton
```

Теперь давайте обернем сериализованный `http.request` в `rldp.query` и сериализируем его тоже:

```
694d798a -- TL ID rldp. ery
184c01cb1a1e4dc9322e5cabe8a2d2a0a4dd82011edaf59eb66f3d4d15b1c5c -- query_id = {random}
0004040000000000-- max_answer_size = 257 KB, может быть любой размер заголовков
258f9063 -- тайм-аут (unix) = 1670418213
34 e191b161116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245 -- данные (http. equest)
   de4711940347455416687474703a2f2f666f756e646174696f6e2e746f6e2f00
   08485454502f312e310000000100000004486f73740000000e666f756e646174
   696f6e2e746f6e00 00000000
```

### Кодирование и отправка пакетов

Теперь нам нужно применить к этим данным алгоритм FEC RaptorQ.

Создадим кодировщик, для чего мы должны превратить результирующий байтовый массив в символы фиксированного размера. В ТОН размер символа составляет 768 байт.
Для этого давайте разделим массив на части 768 байт. В последней части, если он выходит меньше, чем 768, то его нужно подкрепить нулевыми байтами к требуемому размеру.

Наш массив размером 156 байт, это значит, что будет только 1 кусок, и нам нужно поместить его на 612 нулевых байтах в размере 768.

Также для кодировщика выбираются константы в зависимости от размера данных и символа, подробнее об этом вы можете узнать в документации самого RaptorQ, но для того, чтобы не попасть в математический джунгль, я рекомендую использовать готовую библиотеку, которая реализует такую кодировку.
[[Пример создания кодировки]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq/encoder.go#L15) и [[пример кодирования символов]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/raptorq/solver.go#L26).

Символы закодированы и посылаются в стиле округления: мы сначала определяем «seqno», что равно 0, и increment его на 1 для каждого последующего закодированного пакета. Например, если у нас 2 символа, то мы кодируем и высылаем первое, увеличить seqno на 1, затем второй и увеличить seqno на 1, затем снова первый и увеличить seqno, который в данный момент уже равен 2, другой 1.
И так до тех пор, пока мы не получим сообщение о том, что узел принял данные.

Теперь, когда мы создали кодировщик, мы готовы отправить данные, для этого мы заполним схему TL:

```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
```

- `transfer_id` - случайный int256, одинаковый для всех messageParts в рамках одной передачи данных.
- `fec_type` — `fec.raptorQ`.
- - `data_size` = 156
- - `symbol_size` = 768
- - `symbols_count` = 1
- `part` в нашем случае всегда 0, может быть использован для переводов, которые превышают лимит размера.
- `total_size` = 156. Размер наших передаваемых данных.
- `seqno` - для первого пакета будет равен 0, и для каждого последующего пакета он увеличится на 1, будет использоваться в качестве параметра декодирования и символа кодирования.
- `data` - наш кодированный символ, размер 768 байт.

После сериализации `rldp.messagePart`, оберните его в `adnl.message.custom` и отправьте его по ADNL UDP.

Мы отправляем пакеты в цикле, увеличивая seqno все время, пока не ждем `rldp. omplete` сообщение от узла, или мы останавливаемся в тайм-ауте. После того, как мы отправили количество пакетов, равное количеству наших символов, мы можем замедлить и отправить дополнительный пакет, например, один раз в 10 миллисекунд или меньше.
Дополнительные пакеты используются для восстановления в случае потери данных, так как UDP является быстрым, но ненадежным протоколом.

[[Пример реализации]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L249)

### Обработка ответа от 'foundation.ton'

Во время отправки мы уже можем ожидать ответа от сервера, в нашем случае ожидаем `rldp.answer` с `http.response` внутри.
Он придет к нам таким же образом, в виде передачи RLDP, так как он был отправлен на момент запроса, но `transfer_id` будет инвертирован (каждый байт XOR 0xFF).
Мы получим сообщения `adnl.message.custom`, содержащие `rldp.messagePart`.

Сначала нам нужно получить информацию FEC от первого полученного сообщения о переводе, параметры `data_size`, `symbol_size` и `symbols_count` из \`fec. Структура сообщения aptorQ.
Нам нужны их для инициализации декодера RaptorQ. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L137)

После инициализации добавляем принятые символы с их `seqno` в наш декодер, и как только мы накопим минимальное требуемое число, равное `symbols_count`, мы можем попробовать декодировать полное сообщение. В результате мы отправим `rldp.complete`. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L168)

Результатом будет сообщение `rldp.answer` с тем же query_id, что и в отправленном нами `rldp.query`. Данные должны содержать `http.response`.

```tlb
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;
```

С основными полями, я думаю, что все понятно, суть такая же, как в HTTP.
Интересным флагом здесь является `no_payload`, если это правда, то в ответе нет тела (`Content-Length` = 0).
Ответ от сервера можно считать полученным.

Если `no_payload` = false, то содержимое в ответе, и нам нужно его получить.
Для этого нам нужно отправить запрос с `http.getNextPayloadPart` схемой TL в `rldp.query`.

```tlb
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

`id` должен быть таким же, как мы отправили в `http.request`, `seqno` - 0, и +1 для каждой следующей части. `max_chunk_size` — это максимальный размер чанка, который мы готовы принять, обычно используется 128 КБ (131072 байта).

В ответ мы получим:

```tlb
http.payloadPart данные:байты трейлера:(vector http.header) last:Bool = http.PayloadPart;
```

Если `last` = true, то мы достигли конца, мы можем собрать все части вместе и получить полное тело ответа, например, html.

## Справочная литература

_Здесь [ссылка на оригинальную статью](https://github.com/xssnick/ton-deep-doc/blob/master/RLDP.md) от [Oleg Baranov](https://github.com/xssnick)._
