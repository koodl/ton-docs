# ADNL UDP - Internode

ADNL over UDP используется узлами и компонентами TON для общения друг с другом. Это низкоуровневый протокол, на котором управляются другие протоколы TON более высокого уровня, такие как DHT и RLDP.
В этой статье мы узнаем, как работает ADNL над UDP для базовой коммуникации между узлами.

Unlike ADNL over TCP, in the UDP implementation, the handshake takes place in a different form, and an additional layer is used in the form of channels, but other principles are similar:
encryption keys are also generated based on our private key and the peer's public key, which is known in advance from the config or received from other network nodes.

В UDP версии ADNL, соединение устанавливается в то же время с получением начальных данных от узла, если инициатор отправил сообщение "создать канал", будет рассчитан ключ канала и будет подтверждено создание канала.
Когда канал будет установлен, дальнейшая связь будет продолжаться внутри него.

## Структура пакетов и связь

### Первые пакеты

Давайте проанализируем инициализацию соединения с узлом DHT и получение подписанного списка его адресов, чтобы понять, как работает протокол.

Найдите нужный вам узел в [глобальной конфигурации](https://ton-blockchain.github.io/global.config.json) в разделе `dht.nodes`. Например:

```json
{
  "@type": "dht.node",
  "id": {
    "@type": "pub. d25519",
    "key": "fZnkoIAxrTd4xeBgVpZFRm5SvvSx7eN3Vbe8c83YMk="
  },
  "addr_list": {
    "@type": "adnl. Список ddressist",
    "addrs": [
      {
        "@type": "adnl. ddress. dp",
        "ip": 1091897261,
        "порт": 15813
      }
    ],
    "Версия": 0,
    "reinit_date": 0,
    "Приоритет": 0,
    "expire_at": 0
  },
  "версия": -1,
  "Подпись": "cmaMrV/9wuaHOOyXYjoxBnckJktJqrQZ2i+YaY3ehIyiL3LkW81OQ91vm8zzsx1kwwadGZNzgq4hI4PCB/U5Dw=="
}
```

1. Давайте возьмем свой ключ ED25519, `fZnkoIAxrTd4xeBgVpZFRm5SvSx7eN3Vbe8c83YMk`, и расширим его от base64
2. Возьмите IP-адрес `1091897261` и переведите его в понятный формат, используя [service](https://www. rowserling.com/tools/dec-to-ip) или с помощью преобразования в маленькие endian байты, мы получим `65.21.7.173`
3. Комбинируйтесь с портом, найдите `65.21.7.173:15813` и установите UDP соединение.

Мы хотим открыть канал, чтобы общаться с узлом и получить некоторую информацию, и в качестве главной задачи - получать из него список подписанных адресов. Для этого мы создадим 2 сообщения, первое - [создать канал](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L129):

```tlb
adnl.message.createChannel ключ:int256 date:int = adnl.Message
```

У нас есть 2 параметра - ключ и дата. На дату мы укажем текущую метку unix времени. А для ключа - нам нужно сгенерировать новую ED25519 частных+открытых ключей специально для канала, будут использованы для инициализации [открытого ключа шифрования](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh). Мы будем использовать наш сгенерированный открытый ключ в параметре `key` сообщения, и просто сохраним его на данный момент.

Сериализовать заполненную структуру TL и получить:

```
bbc373e6                                                         -- TL ID adnl.message.createChannel 
d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7 -- key
555c8763                                                         -- date
```

Давай перейдем к нашему главному запросу - [получи список адресов](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L198).
Для его выполнения, мы должны сначала сериализовать его структуру TL:

```tlb
dht.getSignedAddressList = dht.Node
```

У него нет параметров, поэтому мы просто сериализуем его. Это будет только его id - `ed4879a9`.

Далее, поскольку это запрос более высокого уровня протокола DHT, мы должны сначала его обработать в структуре TL `adnl.message.query`:

```tlb
adnl.message.query query_id:int256 query:bytes = adnl.Message
```

Как `query_id` мы генерируем случайные 32 байта, как `query` мы используем наш основной запрос, [завернутый в массив байтов](/v3/documentation/data-formats/tl#encoding-bytes-array).
Мы получим:

```
7af98bb4 -- TL ID adnl.message.query
d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875 -- query_id
04 ed4879a9 000000 -- запрос
```

### Создание пакета

Все коммуникации осуществляются с помощью пакетов, содержание которых [структура TL](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L81):

```tlb
adnl.packetContents 
  rand1:bytes                                     -- random 7 or 15 bytes
  flags:#                                         -- bit flags, used to determine the presence of fields further
  from:flags.0?PublicKey                          -- sender's public key
  from_short:flags.1?adnl.id.short                -- sender's ID
  message:flags.2?adnl.Message                    -- message (used if there is only one message)
  messages:flags.3?(vector adnl.Message)          -- messages (if there are > 1)
  address:flags.4?adnl.addressList                -- list of our addresses
  priority_address:flags.5?adnl.addressList       -- priority list of our addresses
  seqno:flags.6?long                              -- packet sequence number
  confirm_seqno:flags.7?long                      -- sequence number of the last packet received
  recv_addr_list_version:flags.8?int              -- address version 
  recv_priority_addr_list_version:flags.9?int     -- priority address version
  reinit_date:flags.10?int                        -- connection reinitialization date (counter reset)
  dst_reinit_date:flags.10?int                    -- connection reinitialization date from the last received packet
  signature:flags.11?bytes                        -- signature
  rand2:bytes                                     -- random 7 or 15 bytes
        = adnl.PacketContents
        
```

Как только мы сериализовали все сообщения, которые мы хотим отправить, мы можем начать создание пакета.
Пакеты для отправки на канал отличаются содержимым пакетов, которые отправляются до инициализации канала.
Сначала давайте проанализируем основной пакет, используемый для инициализации.

Во время первоначального обмена данными вне канала, сериализованная структура содержимого пакета префиксом с открытым ключом пира - 32 байта.
Наш открытый ключ - 32 байта, хеш sha256 сериализованного TL структуры контента - 32 байта.
Содержимое пакета зашифровано с помощью [общего ключа](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh), полученного с нашего приватного ключа и открытого ключа сервера.

Сериализовать структуру содержимого пакетов и разобрать его байт по байту:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 4e0e7dd6d0c5646c204573bc47e567                                      -- rand1, 15 (0f) random bytes
d9050000                                                               -- flags (0x05d9) -> 0b0000010111011001
                                                                       -- from (present because flag's zero bit = 1)
c6b41348                                                                  -- TL ID pub.ed25519
   afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6       -- key:int256
                                                                       -- messages (present because flag's third bit = 1)
02000000                                                                  -- vector adnl.Message, size = 2 messages   
   bbc373e6                                                                  -- TL ID adnl.message.createChannel
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7          -- key
   555c8763                                                                  -- date (date of creation)
   
   7af98bb4                                                                  -- TL ID [adnl.message.query](/)
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875          -- query_id
   04 ed4879a9 000000                                                        -- query (bytes size 4, padding 3)
                                                                       -- address (present because flag's fourth bit = 1), without TL ID since it is specified explicitly
00000000                                                                  -- addrs (empty vector, because we are in client mode and do not have an address on wiretap)
555c8763                                                                  -- version (usually initialization date)
555c8763                                                                  -- reinit_date (usually initialization date)
00000000                                                                  -- priority
00000000                                                                  -- expire_at

0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0000000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
555c8763                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
555c8763                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
00000000                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
0f 2b6a8c0509f85da9f3c7e11c86ba22                                      -- rand2, 15 (0f) random bytes
```

После сериализации - нам нужно подписать полученный байтовый массив с ключом ED25519, который мы создали и сохранили ранее.
После того, как мы сгенерировали подпись (64 байта в размере), мы должны добавить ее в пакет, сериализовать его снова, но теперь добавить 11-й бит к флагу, что означает наличие подписи:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 4e0e7dd6d0c5646c204573bc47e567                                      -- rand1, 15 (0f) random bytes
d90d0000                                                               -- flags (0x0dd9) -> 0b0000110111011001
                                                                       -- from (present because flag's zero bit = 1)
c6b41348                                                                  -- TL ID pub.ed25519
   afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6       -- key:int256
                                                                       -- messages (present because flag's third bit = 1)
02000000                                                                  -- vector adnl.Message, size = 2 message   
   bbc373e6                                                                  -- TL ID adnl.message.createChannel
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7          -- key
   555c8763                                                                  -- date (date of creation)
   
   7af98bb4                                                                  -- TL ID adnl.message.query
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875          -- query_id
   04 ed4879a9 000000                                                        -- query (bytes size 4, padding 3)
                                                                       -- address (present because flag's fourth bit = 1), without TL ID since it is specified explicitly
00000000                                                                  -- addrs (empty vector, because we are in client mode and do not have an address on wiretap)
555c8763                                                                  -- version (usually initialization date)
555c8763                                                                  -- reinit_date (usually initialization date)
00000000                                                                  -- priority
00000000                                                                  -- expire_at

0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0000000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
555c8763                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
555c8763                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
00000000                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
40 b453fbcbd8e884586b464290fe07475ee0da9df0b8d191e41e44f8f42a63a710    -- signature (present because flag's eleventh bit = 1), (bytes size 64, padding 3)
   341eefe8ffdc56de73db50a25989816dda17a4ac6c2f72f49804a97ff41df502    --
   000000                                                              --
0f 2b6a8c0509f85da9f3c7e11c86ba22                                      -- rand2, 15 (0f) random bytes
```

Теперь у нас есть собранный, подписанный и сериализованный пакет, который представляет собой массив байт.
Для последующей проверки целостности получателем необходимо вычислить sha256 хэш пакета. Например, давайте `408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2`.

Теперь давайте зашифруем содержимое нашего пакета шифром AES-CTR, используя [общий ключ](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh), получен с нашего закрытого ключа и публичного ключа узла (не ключа канала).

Мы почти готовы к отправке, осталось [вычислить ID](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-key-id) ключа пира ED25519 и объединиться все вместе:

```
daa76538d99c79ea097a67086ec05acca12d1fefdbc9c96a76ab5a12e66c7ebb -- ID ключа сервера
afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6 -- наш публичный ключ
408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2 -- sha256 хэш содержимого (до шифрования)
. -- зашифрованное содержимое пакета
```

Теперь мы можем отправить наш построенный пакет пиру по UDP и ждать ответа.

В ответ мы получим пакет с аналогичной структурой, но с различными сообщениями. Он будет состоять из:

```
68426d4906bafbd5fe25baf9e0608cf24fffa7eca0aece70765d64f61f82f005 -- ID нашего ключа
2d11e4a08031ad3778c5e060569645466e52bd1bd2c7b78ddd56def1cf3760c9 -- публичный ключ сервера, для общего ключа
f32fa6286d8ae61c0588b5a03873a220a3163cad2293a5dace5f03f06681e88a -- хэш контента sha256 (до шифрования)
. . -- зашифрованное содержимое пакета
```

Десериализация пакета с сервера является следующим:

1. Мы проверяем идентификатор ключа из пакета, чтобы понять, что пакет для нас.
2. Используя открытый ключ сервера из пакета и наш закрытый ключ, мы вычисляем общий ключ и расшифровываем содержимое пакета
3. Сравните отправленный нам хеш sha256 с хэшем полученным из расшифрованных данных, он должен совпадать
4. Начало десериализации содержимого пакетов с помощью схемы `adnl.packetContents` TL

Содержимое пакета будет выглядеть следующим образом:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 985558683d58c9847b4013ec93ea28                                      -- rand1, 15 (0f) random bytes
ca0d0000                                                               -- flags (0x0dca) -> 0b0000110111001010
daa76538d99c79ea097a67086ec05acca12d1fefdbc9c96a76ab5a12e66c7ebb       -- from_short (because flag's first bit = 1)
02000000                                                               -- messages (present because flag's third bit = 1)
   691ddd60                                                               -- TL ID adnl.message.confirmChannel 
   db19d5f297b2b0d76ef79be91ad3ae01d8d9f80fab8981d8ed0c9d67b92be4e3       -- key (server channel public key)
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7       -- peer_key (our public channel key)
   94848863                                                               -- date
   
   1684ac0f                                                               -- TL ID adnl.message.answer 
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875       -- query_id
   90 48325384c6b413487d99e4a08031ad3778c5e060569645466e52bd5bd2c7b       -- answer (the answer to our request, we will analyze its content in an article about DHT)
      78ddd56def1cf3760c901000000e7a60d67ad071541c53d0000ee354563ee       --
      35456300000000000000009484886340d46cc50450661a205ad47bacd318c       --
      65c8fd8e8f797a87884c1bad09a11c36669babb88f75eb83781c6957bc976       --
      6a234f65b9f6e7cc9b53500fbe2c44f3b3790f000000                        --
      000000                                                              --
0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0100000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
94848863                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
ee354563                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
94848863                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
40 5c26a2a05e584e9d20d11fb17538692137d1f7c0a1a3c97e609ee853ea9360ab6   -- signature (present because flag's eleventh bit = 1), (bytes size 64, padding 3)
   d84263630fe02dfd41efb5cd965ce6496ac57f0e51281ab0fdce06e809c7901     --
   000000                                                              --
0f c3354d35749ffd088411599101deb2                                      -- rand2, 15 (0f) random bytes
```

Сервер ответил нам двумя сообщениями: `adnl.message.confirmChannel` и `adnl.message.answer`.
С `adnl.message.answer` все просто, это ответ на наш запрос `dht.getSignedAddressList`, мы проанализируем его в статье о DHT.

Давайте сосредоточимся на `adnl.message.confirmChannel`, что означает, что узел подтвердил создание канала и отправил нам свой публичный ключ канала. Теперь, имея ключ нашего закрытого канала и ключ публичного канала узла, мы можем посчитать [общий ключ](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh).

Теперь, когда мы рассчитали ключ общего канала, необходимо вывести из него 2 ключа - один для шифрования исходящих сообщений, другой для расшифровки входящих сообщений.
Выделение 2 ключей из них довольно просто, второй ключ равен общему ключу, написанному в обратном порядке. Например:

```
Общий ключ : AABB2233

Первый ключ: AABB2233
Второй ключ: 3322BBAA
```

Остается определить, какой ключ использовать для чего; мы можем это сделать, сравнив идентификатор ключа нашего публичного канала с идентификатором публичного ключа канала сервера, преобразование их в числовую форму - uint256. Этот подход используется для того, чтобы убедиться в том, что и сервер, и клиент определяют какой ключ использовать для чего. Если сервер использует первый ключ для шифрования, то с таким подходом клиент всегда будет использовать его для расшифровки.

Условия использования:

```
The server id is smaller than our id:
Encryption: First Key
Decryption: Second Key

The server id is larger than our id:
Encryption: Second Key
Decryption: First Key

If the ids are equal (nearly impossible):
Encryption: First Key
Decryption: First Key
```

[[Implementation example]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/adnl.go#L502)

### Связь в канале

Все последующие обмены пакетами будут происходить внутри канала, а ключи каналов будут использоваться для шифрования.
Давайте отправим этот же запрос `dht.getSignedAddressList` внутри вновь созданного канала, чтобы увидеть разницу.

Давайте построим пакет для канала с использованием той же структуры `adnl.packetContents`:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f c1fbe8c4ab8f8e733de83abac17915                                      -- rand1, 15 (0f) random bytes
c4000000                                                               -- flags (0x00c4) -> 0b0000000011000100
                                                                       -- message (because second bit = 1)
7af98bb4                                                                  -- TL ID adnl.message.query
fe3c0f39a89917b7f393533d1d06b605b673ffae8bbfab210150fe9d29083c35          -- query_id
04 ed4879a9 000000                                                        -- query (our dht.getSignedAddressList packed in bytes with padding 3)
0200000000000000                                                       -- seqno (because flag's sixth bit = 1), 2 because it is our second message
0100000000000000                                                       -- confirm_seqno (flag's seventh bit = 1), 1 because it is the last seqno received from the server
07 e4092842a8ae18                                                      -- rand2, 7 (07) random bytes
```

Пакеты в канале достаточно просты и по сути состоят из последовательностей (seqno) и самих сообщений.

После сериализации, как и в прошлый раз, мы подсчитываем хеш sha256 пакета. Затем мы шифруем пакет, используя ключ, предназначенный для исходящих пакетов канала.
[Calculate](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-key-id) `pub.aes` ID ключа шифрования наших исходящих сообщений, и мы строим наш пакет:

```
bcd1cf47b9e657200ba21d94b822052cf553a548f51f539423c8139a83162180 -- ID ключа шифрования наших исходящих сообщений 
6185385aeee5faae7992eb350f26ba253e8c7c5fa1e3e1879d9a0666b9bd6080 -- sha256 хэш содержимого (до шифрования)
. . -- зашифрованное содержимое пакета
```

Мы отправляем пакет через UDP и ожидаем ответа. В ответ мы получим пакет того же типа, который мы отправили (те же поля), но с ответом на наш запрос `dht.getSignedAddressList`.

## Другие типы сообщений

Для базовой коммуникации такие сообщения, как `adnl.message.query` и `adnl.message. Используется nswer`, о котором мы говорили выше, но для некоторых ситуаций также используются другие типы сообщений, которые мы обсудим в этом разделе.

### adnl.message.part

Этот тип сообщения является частью одного из других возможных типов сообщений, таких как `adnl.message.answer`. Этот метод передачи данных используется, когда сообщение слишком велико для передачи в одном UDP-датаграмме.

```tlb
adnl.message. art 
hash:int256 -- sha256 hash of the original message
total_size:int -- оригинальный размер сообщения
offset:int -- смещение согласно началу исходного сообщения
data:bytes -- часть данных оригинального сообщения
   = adnl. произношение;
```

Таким образом, для того чтобы собрать оригинальное сообщение, нам нужно получить несколько частей, и в соответствии с смещениями, котируйте их в одинарный массив.
И затем обрабатывать его как сообщение (согласно префиксу ID в массиве байтов).

### adnl.message.custom

```tlb
adnl.message.custom data:bytes = adnl.Message;
```

Такие сообщения используются, когда логика на более высоком уровне не соответствует формату ответа запроса, сообщения этого типа позволяют полностью переместить обработку на более высокий уровень, так как сообщение несет только массив байтов, без query_id и других полей.
Сообщения этого типа используются, например, в RLDP, так как может быть только один ответ на множество запросов, эта логика управляется самим RLDP.

### Заключение

Дальнейшее сообщение осуществляется на основе логики, описанной в настоящей статье,
но содержимое пакетов зависит от протоколов более высокого уровня, таких как DHT и RLDP.

## Справочная литература

_Здесь [ссылка на оригинальную статью](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-UDP-Internal.md) от [Oleg Baranov](https://github.com/xssnick)._
