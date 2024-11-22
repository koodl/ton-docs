# Кросс-цепные мосты

Децентрализованные перекрестные мосты работают на TON Blockchain, позволяя передавать активы из TON Blockchain в другие блокчейны и наоборот.

## Мост Тонкона

Мост Тонкон позволяет передавать Тонкон между Тонконом блокчейном и блокчейном Ethereum, а также между TON Blockchain и BNB Smart Chain.

Мост управляется [децентрализованными оракулами](/v3/documentation/infra/crosschain/bridge-addresses).

### Как это использовать?

Ведущий мост размещен на https://ton.org/bridge.

:::info
[Исходный код фронтенда моста](https://github.com/ton-blockchain/bridge)
:::

### Исходные коды смарт-контрактов TON-Ethereum

- [Функ (сторона TON)](https://github.com/ton-blockchain/bridge-func)
- [Солидарность (сторона эфира)](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

### исходные коды умных цепей TON-BNB Smart Chain

- [Функ (сторона TON)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [Солидарность (сторона BSC)](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### Конфигурация блокчейна

Вы можете получить фактические адреса смарт-контракта моста и адреса оракула, просмотрев соответствующую конфигурацию:

TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738).

БСКЗ: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739).

TON-Polygon: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740).

### Документация

- [Как работает мост](https://github.com/ton-blockchain/TIPs/issues/24)

### Карта перекрёстного пути

- https://t.me/tonblockchain/146
