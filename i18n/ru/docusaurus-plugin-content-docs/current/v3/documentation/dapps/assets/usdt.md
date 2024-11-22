Импортировать кнопку из '@site/src/components/button'

# USDT обработка

## Tether

Стаблекуины - это тип криптовалюты, значение которых 1:1 привязано к другому активу, Например, фиатная валюта или золото для поддержания стабильной цены. До недавнего времени был токен jUSDT, завернутый ERC-20 из токена Ethereum, моста с <a href="https://bridge.ton.org" target="_blank">bridge.ton.org</a>. Но на [18.04.2023](https://t.me/toncoin/824) произошел публичный запуск **родного** USD<unk> token выпущенного компанией <a href="https://tether.to/en/" target="_blank">Tether</a>. После запуска USD<unk> , jUSDT переехал на второй токен приоритета, но до сих пор используется в сервисах в качестве альтернативы или дополнения к USD<unk> .

В TON Blockchain USD<unk> поддерживается как [Jetton Asset](/v3/guidelines/dapps/asset-processing/jettons).

:::info
Чтобы интегрировать Токен Tether USD<unk> в TON Blockchain используйте контрактный адрес:
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>Активы SDK</Button>
<Button href="/v3/guidelines/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>Jetton Processing</Button>
<Button href="https://github.com/ton-community/tma-usdt-payments-demo?tab=readme-ov-file#tma-usdt-payments-demo" colorType={'secondary'} sizeType={'sm'}>Демо платежей TMA USDT</Button>

## Преимущества USD<unk> on TON

### Интеграция с Seamless Telegram

[USD<unk> on TON](https://ton.org/borderless) будет легко интегрироваться в Telegram, предлагая уникальный удобный опыт, который позиционирует TON как наиболее удобный блокчейн для транзакций USDt. Эта интеграция упростит DeFi для пользователей Telegram, сделав его более доступным и понятным.

### Снижение комиссии за транзакции

Комиссия потребляемая Ethereum USD<unk> передача рассчитывается динамически в зависимости от нагрузки на сеть. Вот почему транзакция может стоить много.

```cpp
транзакция_сбор = gas_used * цена
```

- `gas_used` - это сумма газа, используемая во время совершения сделки.
- Цена `gas_price` на 1 единицу газа в Гвейе, рассчитываемая динамически

С другой стороны, средняя комиссия за отправку любого количества USD<unk> в TON Blockchain составляет около 0,0145 TON. Даже если цена TON увеличится 100 раз, транзакции [останутся ультра-дешевыми](/v3/documentation/smart-contracts/transaction-fees#average-transaction-cost). Команда разработчиков TON оптимизировала умный контракт Tether и в три раза дешевле, чем любой другой Jetton.

### Быстрее и масштабируемое

Высокая пропускная способность TON и быстрое время подтверждения позволяют обрабатывать USD<unk> транзакции быстрее, чем когда-либо ранее.

## Дополнительные сведения

:::caution ВАЖНОЕ
В TON Blockchain Jettons можно создавать с одинаковыми именами. Технически он никак не будет отличаться от реального USD<unk> но не будет иметь никакого значения из-за отсутствия безопасности. Вы можете проверить его на мошенничество только проверяя адрес Jetton Master.

See important [recommendations](/v3/guidelines/dapps/asset-processing/jettons).
:::

## Смотреть также

- [Обработка платежей](/v3/guidelines/dapps/asset-processing/payments-processing)
