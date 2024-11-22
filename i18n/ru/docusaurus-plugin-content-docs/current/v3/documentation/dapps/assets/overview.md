импортировать кнопку из '@site/src/components/button'
импортировать вкладки из '@theme/Tabs';
импортировать вкладки из '@theme/TabItem';

# Обзор обработки активов

Здесь вы можете найти **краткий обзор** о [как работают передачи TON](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions), какие [типы активов](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton) вы можете найти в TON (и что насчет того, что вы читаете [next](/v3/documentation/dapps/assets/overview#read-next)) и как [взаимодействовать с тоном](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain) с использованием вашего языка программирования, рекомендуется понять всю информацию, полученную ниже, перед тем как перейти на следующие страницы.

## Обзор сообщений и транзакций

Внедрение полностью асинхронного подхода TON Blockchain включает в себя несколько концепций, которые редки традиционным блокчейнам. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred [messages](/v3/documentation/smart-contracts/message-management/messages-and-transactions) between smart contracts and/or the external world. Каждая транзакция состоит из одного входящего сообщения и до 255 исходящих сообщений.

Есть 3 типа сообщений, которые полностью описаны [here](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages). Коротко положить его:

- [внешнее сообщение](/v3/documentation/smart-contracts/message-management/external-messages):
  - `external in message` (иногда называется просто `external message`) это сообщение, которое отправляется из _outside_ блокчейна на смарт-контракт _inside_ блокчейна.
  - `external out message` (обычно называется `logs message`) отправляется из _blockchain entity_ в _внешний мир_.
- [внутреннее сообщение](/v3/documentation/smart-contracts/message-management/internal-messages) отправляется из одной _blockchain entity_ на _другой_, может переносить некоторое количество цифровых активов и произвольную часть данных.

Общий путь любого взаимодействия начинается с внешнего сообщения, отправленного в «кошелёк» смарт-контракт, , который аутентифицирует отправителя сообщения с помощью публичной криптографии, принимает оплату за оплату и посылает внутренние блокчейн сообщения. Очередь сообщений формирует направленный циклический график, или дерево.

Например:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- `Alice` используйте например [Tonkeeper](https://tonkeeper.com/) для отправки `external message` на её кошелёк.
- `внешнее сообщение` — это входящее сообщение для контракта `кошелек A v4` с пустым источником (сообщение из нигде не было, например [Tonkeeper](https://tonkeeper.com/)).
- `исходящее сообщение` - это выходное сообщение для контракта `кошелек A v4` и входящее сообщение для контракта `кошелек B v4` с источником `кошелек A v4` и `кошелек B v4`.

В результате есть 2 транзакции с набором входящих и выходящих сообщений.

Каждое действие, когда контракт принимает сообщение как входное (инициируемое имя), обрабатывает его и генерирует или не генерирует исходящие сообщения как выходные, называемые «транзакция». Read more about transactions [here](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction).

Эта «транзакция» может длиться **длительный период** времени. Технически транзакции с очередями сообщений агрегируются в блоки, обрабатываемые валидаторами. Асинхронный характер цепочки TON Blockchain **не позволяет предсказать хэш и lt (логическое время) транзакции** на этапе отправки сообщения.

«Транзакция» принята к блоку окончательной и не может быть изменена.

:::info Подтверждение транзакции
TON транзакции необратимы после одного подтверждения. Для лучшего удобства пользователя рекомендуется избегать ожидания дополнительных блоков после завершения транзакций на TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

Smart contracts pay several types of [fees](/v3/documentation/smart-contracts/transaction-fees/fees) for transactions (usually from the balance of an incoming message, behavior depends on [message mode](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes)). Сумма вознаграждения зависит от конфигурации рабочей цепочки с максимальными комиссиями на «masterchain» и значительно меньшими комиссиями на «basechain».

## Типы цифровых активов на TON

TON имеет три типа цифровых активов.

- Toncoin, главный токен сети. Он используется для всех основных операций на блокчейне, например, для оплаты газовых сборов или размещения на проверку.
- Контрактные активы, такие как токены и NFT, которые схожи со стандартами ERC-20/ERC-721 и управляются произвольными контрактами и поэтому могут потребовать таможенных правил для обработки. Вы можете найти больше информации о его обработке в [process NFTs](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) и [process Jettons](/v3/guidelines/dapps/asset-processing/jettons) статьях.
- Родной токен, который является особым видом активов, которые могут быть прикреплены к любому сообщению в сети. Но эти активы в настоящее время не используются, поскольку функциональность для выпуска новых родных токенов закрыта.

## Взаимодействие с TON блокчейном

Основные операции по TON Blockchain могут проводиться через TonLib. Это общая библиотека, которая может быть скомпилирована вместе с узлом TON и раскрыта API для взаимодействия с блокчейном через так называемые литовые сервера (сервера для простых клиентов). TonLib придерживается бездостоверного подхода, проверяя достоверность всех входящих данных; поэтому нет необходимости в надежном поставщике данных. Доступные методы TonLib перечислены [в схеме TL](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). Они могут использоваться либо в качестве общей библиотеки через [wrappers](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks).

## Читать далее

После прочтения этой статьи вы можете проверить:

1. [Процесс платежей](/v3/guidelines/dapps/asset-processing/payments-processing), чтобы узнать, как работать с `TON coins`
2. [Процесс Jetton](/v3/guidelines/dapps/asset-processing/jettons), чтобы узнать, как работать с `jettons` (то есть `tokens`)
3. [NFT обработка](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) чтобы узнать, как работать с `NFT` (это особый тип `jetton`)
