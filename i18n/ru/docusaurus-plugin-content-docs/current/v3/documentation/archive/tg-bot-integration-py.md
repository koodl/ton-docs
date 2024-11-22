Импортировать кнопку из '@site/src/components/button'

# TON Connect for Telegram Bots - Python

:::warning устаревшее
В этом руководстве описывается устаревший метод интеграции TON Connect с Telegram Bots. Для более безопасного и современного подхода попробуйте использовать [Telegram Mini Apps](/v3/guidelines/dapps/tma/overview для более современной и безопасной интеграции.
:::

В этом руководстве мы создадим образец телеграммы бота, который поддерживает TON Connect 2.0 аутентификацию с помощью Python TON Connect SDK [pytonconnect](https://github.com/XaBbl4/pytonconnect).
Мы анализируем подключение кошелька, отправку транзакции, получение данных о подключенном кошельке и отключение кошелька.

<Button href="https://t.me/test_tonconnect_bot" colorType={'primary'} sizeType={'sm'}>

Открыть демо бота

</Button>

<Button href="https://github.com/yungwine/ton-connect-bot" colorType={'secondary'} sizeType={'sm'}>

Check out GitHub

</Button>

## Подготовка

### Установить библиотеки

Чтобы заставить бота использовать `aiogram` 3.0 Python библиотеку.
Чтобы начать интеграцию TON Connect в ваш Telegram bot, необходимо установить пакет `pytonconnect`.
И для использования примитивов TON и разбора адреса пользователя нам нужно `pytoniq-core`.
Вы можете использовать Pip для этой цели:

```bash
pip установить aiogram pytoniq-core python-dotenv
pip install pytonconnect
```

### Настройка конфигурации

Укажите в файле `.env` [токен бота](https://t.me/BotFather) и ссылку на файл TON Connect [манифест](https://github.com/ton-connect/sdk/tree/main/packages/sdk#add-the-tonconnect-manifest). После загрузки в `config.py`:

```dotenv
# .env

TOKEN='1111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  # your bot token here
MANIFEST_URL='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json'
```

```python
# config.py

из os импортировать как env

из dotenv импортировать load_dotenv
load_dotenv()

TOKEN = env['TOKEN']
MANIFEST_URL = env['MANIFEST_URL']
```

## Создать простого бота

Создайте файл `main.py`, который будет содержать основной код бота:

```python
# main.py

import sys
import logging
import asyncio

import config

from aiogram import Bot, Dispatcher, F
from aiogram. numes of import ParseMode
from aiogram. ilters import CommandStart, Command
из aiogram.types import Message, CallbackQuery


logger = logging. etLogger(__file__)

dp = Dispatcher()
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
    

@dp. essage(CommandStart())
async def command_start_handler(message: Message):
    ожидает сообщения. nswer(text='Привет!')

async def main() -> Нет:
    ожидает бота. elete_webhook(drop_pending_updates=True) # skip_updates = True
    await dp. tart_polling(bot)


if __name__ == "__main__":
    журналирования. asicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

```

## Подключение к кошельку

### Хранилище подключения TON

Давайте создадим простое хранилище для TON Connect

```python
# tc_storage.py

from pytonconnect.storage import IStorage, DefaultStorage


storage = {}


class TcStorage(IStorage):

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def _get_key(self, key: str):
        return str(self.chat_id) + key

    async def set_item(self, key: str, value: str):
        storage[self._get_key(key)] = value

    async def get_item(self, key: str, default_value: str = None):
        return storage.get(self._get_key(key), default_value)

    async def remove_item(self, key: str):
        storage.pop(self._get_key(key))

```

### Обработчик соединения

Во-первых, нам нужна функция, которая возвращает разные экземпляры для каждого пользователя:

```python
# connector.py

from pytonconnect import TonConnect

import config
from tc_storage import TcStorage


def get_connector(chat_id: int):
    return TonConnect(config.MANIFEST_URL, storage=TcStorage(chat_id))
 

```

Давай добавим обработчик подключения в `command_start_handler()`:

```python
# main.py

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    chat_id = message. hat.id
    коннектор = get_connector(chat_id)
    подключён = ожидающий коннектор. estore_connection()

    mk_b = InlineKeyboardBuilder()
    при подключении:
        mk_b. utton(text='Send Transaction', callback_data='send_tr')
        mk_b.button(text='Disconnect', callback_data='disconnect')
        ожидает сообщения. nswer(text='Вы уже подключены!', reply_markup=mk_b.as_markup())
    else:
        wallets_list = TonConnect. et_wallets()
        для кошелька в wallets_list:
            mk_b. utton(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
        mk_b. djust(1, )
        await message.answer(text='Выберите кошелек для подключения', reply_markup=mk_b.as_markup())

```

Теперь для пользователя, который еще не подключился к кошельку, бот отправляет сообщение с кнопками для всех доступных кошельков.
Поэтому нам нужно написать функцию `connect:{wallet["name"]}` callbacks:

```python
# main.py

async def connect_wallet(message: Message, wallet_name: str):
    connector = get_connector(message.chat.id)

    wallets_list = соединитель. et_wallets()
    кошелек = Нет

    для w в кошельке:
        if w['name'] == wallet_name:
            кошелек = w

    если кошелек пуст:
        raise Exception(f'Неизвестный кошелек: {wallet_name}')

    generated_url = await connector. onnect(wallet)

    mk_b = InlineKeyboardBuilder()
    mk_b. utton(text='Connect', url=generated_url)

    await message.answer(text='Подключить кошелек в течение 3 минут', reply_markup=mk_b. s_markup())

    mk_b = InlineKeyboardBuilder()
    mk_b. utton(text='Start', callback_data='start')

    для i в диапазоне (1, 180):
        ожидают асинсио. leep(1)
        если коннектор. подключено:
            если connector.account. ddress:
                wallet_address = connector.account. ddress
                wallet_address = Address(wallet_address). o_str(is_bounceable=False)
                ожидает сообщения. nswer(f'Вы подключены к адресу <code>{wallet_address}</code>', reply_markup=mk_b. s_markup())
                логгер. nfo(f'Connected with address: {wallet_address}')
            return

    await message. nswer(f'Timeout error!', reply_markup=mk_b. s_markup())


@dp.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call. nswer()
    message = call.message
    data = call. ata
    if data == "start":
        await command_start_handler(message)
    elif data == "send_tr":
        await send_transaction(message)
    elif data == 'disconnect':
        await disconnect_wallet(message)
    else:
        данные = данные. plit(':')
        если данные[0] == 'connect':
            ожидают connect_wallet(сообщение, данные[1])
```

Бот предоставляет пользователю 3 минуты для подключения кошелька, после чего сообщает об ошибке.

## Выполнить запрос транзакции

Давайте возьмем один пример из [сборщиков сообщений](/v3/guidelines/ton-connect/guidelines/preparing-messages) статьи:

```python
# messages.py

from base64 import urlsafe_b64encode

from pytoniq_core import begin_cell


def get_comment_message(destination_address: str, amount: int, comment: str) -> dict:

    data = {
        'address': destination_address,
        'amount': str(amount),
        'payload': urlsafe_b64encode(
            begin_cell()
            .store_uint(0, 32)  # op code for comment message
            .store_string(comment)  # store comment
            .end_cell()  # end cell
            .to_boc()  # convert it to boc
        )
        .decode()  # encode it to urlsafe base64
    }

    return data

```

И добавьте функцию `send_transaction()` в файл `main.py`:

```python
# main.py

@dp.message(Command('transaction'))
async def send_transaction(message: Message):
    connector = get_connector(message. hat.id)
    подключено = ожидающий соединитель. estore_connection()
    , если не подключено:
        ожидает сообщения. nswer('Подключить кошелек сначала! )
        return
    
    transaction = {
        'valid_until': int(time. ime() + 3600),
        'messages': [
            get_comment_message(
                destination_address='0:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                amount=int(0. 1 * 10 ** 9),
                comment='hello world!
            )
        ]
    }

    ожидает сообщения. nswer(text='Подтвердите транзакцию в вашем приложении кошелька!')
    ожидают подключения. end_transaction(
        транзакция
)
```

Но нам также следует обработать возможные ошибки, поэтому мы обернем метод `send_transaction` в заявление `try - except`:

```python
@dp.message(Command('transaction'))
async def send_transaction(message: Message):
    ...
    ожидает сообщения. nswer(text='Подтвердить транзакцию в вашем приложении кошелька!')
    try:
        ждут asyncio. ait_for(коннектор). end_transaction(
            транзакция=транзакция
        ), 300)
    кроме асинчио. imeoutError:
        ожидает message.answer(text='Timeout error!')
    кроме pytonconnect. xceptions.UserRejectsError:
        ожидает сообщения. nswer(text='Вы отклонили транзакцию!')
    за исключением исключения как e:
        ожидают сообщения. nswer(text=f'Неизвестная ошибка: {e}')
```

## Добавить обработчик отключения

Реализация этой функции достаточно проста:

```python
async def disconnect_wallet(message: Message):
    connector = get_connector(message.chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    await message.answer('Вы были успешно отключены!')
```

В настоящее время проект имеет следующую структуру:

```bash
.
.env
├── config.py
├── connector.py
├── main.py
├── messages.py
└── tc_storage.py
```

И `main.py` выглядит так:

<details>
<summary>Show main.py</summary>

```python
# main.py

import sys
import logging
import asyncio
import time

import pytonconnect.exceptions
from pytoniq_core import Address
from pytonconnect import TonConnect

import config
from messages import get_comment_message
from connector import get_connector

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


logger = logging.getLogger(__file__)

dp = Dispatcher()
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    mk_b = InlineKeyboardBuilder()
    if connected:
        mk_b.button(text='Send Transaction', callback_data='send_tr')
        mk_b.button(text='Disconnect', callback_data='disconnect')
        await message.answer(text='You are already connected!', reply_markup=mk_b.as_markup())

    else:
        wallets_list = TonConnect.get_wallets()
        for wallet in wallets_list:
            mk_b.button(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
        mk_b.adjust(1, )
        await message.answer(text='Choose wallet to connect', reply_markup=mk_b.as_markup())


@dp.message(Command('transaction'))
async def send_transaction(message: Message):
    connector = get_connector(message.chat.id)
    connected = await connector.restore_connection()
    if not connected:
        await message.answer('Connect wallet first!')
        return

    transaction = {
        'valid_until': int(time.time() + 3600),
        'messages': [
            get_comment_message(
                destination_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                amount=int(0.01 * 10 ** 9),
                comment='hello world!'
            )
        ]
    }

    await message.answer(text='Approve transaction in your wallet app!')
    try:
        await asyncio.wait_for(connector.send_transaction(
            transaction=transaction
        ), 300)
    except asyncio.TimeoutError:
        await message.answer(text='Timeout error!')
    except pytonconnect.exceptions.UserRejectsError:
        await message.answer(text='You rejected the transaction!')
    except Exception as e:
        await message.answer(text=f'Unknown error: {e}')


async def connect_wallet(message: Message, wallet_name: str):
    connector = get_connector(message.chat.id)

    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')

    generated_url = await connector.connect(wallet)

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Connect', url=generated_url)

    await message.answer(text='Connect wallet within 3 minutes', reply_markup=mk_b.as_markup())

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Start', callback_data='start')

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                await message.answer(f'You are connected with address <code>{wallet_address}</code>', reply_markup=mk_b.as_markup())
                logger.info(f'Connected with address: {wallet_address}')
            return

    await message.answer(f'Timeout error!', reply_markup=mk_b.as_markup())


async def disconnect_wallet(message: Message):
    connector = get_connector(message.chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    await message.answer('You have been successfully disconnected!')


@dp.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call.answer()
    message = call.message
    data = call.data
    if data == "start":
        await command_start_handler(message)
    elif data == "send_tr":
        await send_transaction(message)
    elif data == 'disconnect':
        await disconnect_wallet(message)
    else:
        data = data.split(':')
        if data[0] == 'connect':
            await connect_wallet(message, data[1])


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates = True
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

```

</details>

## Улучшение

### Добавить постоянное хранилище - Redis

В настоящее время TON Connect Storage использует dict, который приводит к потере сеансов после перезапуска бота.
Давайте добавим постоянное хранилище данных с помощью Redis:

После запуска базы данных Redis установите библиотеку python для взаимодействия с ней:

```bash
pip установить redis
```

И обновите класс `TcStorage` в `tc_storage.py`:

```python
import redis.asyncio as redis

client = redis.Redis(host='localhost', port=6379)


class TcStorage(IStorage):

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def _get_key(self, key: str):
        return str(self.chat_id) + key

    async def set_item(self, key: str, value: str):
        await client.set(name=self._get_key(key), value=value)

    async def get_item(self, key: str, default_value: str = None):
        value = await client.get(name=self._get_key(key))
        return value.decode() if value else default_value

    async def remove_item(self, key: str):
        await client.delete(self._get_key(key))
```

### Add QR Code

Установите пакет python `qrcode` для их создания:

```bash
pip установить qrcode
```

Измените функцию `connect_wallet()` так, что она генерирует qrcode и отправляет его как фото пользователю:

```python
from io import BytesIO
import qrcode
from aiogram.types import BufferedInputFile


async def connect_wallet(message: Message, wallet_name: str):
    . .
    
    img = qrcode. ake(generated_url)
    stream = BytesIO()
    img. ave(stream)
    файл = BufferedInputFile(file=stream.getvalue(), filename='qrcode')

    ожидает сообщения. nswer_photo(photo=file, caption='Подключить кошелек в течение 3 минут', reply_markup=mk_b.as_markup())
    
...
```

## Summary

Что дальше?

- Вы можете добавить улучшенную обработку ошибок в боте.
- Вы можете добавить начальный текст и что-то вроде команды `/connect_wallet`.

## Смотреть также

- [Полный код бота](https://github.com/yungwine/ton-connect-bot)
- [Подготовка сообщений](/v3/guidelines/ton-connect/guidelines/preparing-messages)
