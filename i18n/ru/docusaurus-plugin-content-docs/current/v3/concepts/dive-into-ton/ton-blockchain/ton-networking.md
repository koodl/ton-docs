# ТЕН Сети

Проект TON использует собственные протоколы к сети между peer-to-peer.

- **TON Blockchain использует эти протоколы** для распространения новых блоков, отправки и сбора кандидатов транзакций и так далее.

  While the networking demands of single-blockchain projects, such as Bitcoin or Ethereum, can be met quite easily (one essentially needs to construct
  a peer-to-peer overlay network and then propagate all new blocks and
  transaction candidates via a [gossip](https://en.wikipedia.org/wiki/Gossip_protocol) protocol), whereas multi-blockchain projects, such
  as TON, are much more demanding (e.g. one must be able to
  subscribe to updates of only some shardchains, not necessarily all of them).

- **TON Ecosystem (например: TON Proxy, TON Sites, TON Storage) работает по этим протоколам.**

  Once the more sophisticated network protocols needed
  to support TON Blockchain are in place, it turns out that they can easily
  be used for purposes not necessarily related to the immediate demands of the
  blockchain itself, thus providing more possibilities and flexibility for creating
  new services in the TON Ecosystem.

## Смотреть также

- [Протокол ADNL](/v3/documentation/network/protocols/adnl/overview)
- [Наложение подсетей](/v3/documentation/network/protocols/overlay)
- [RLDP Протокол](/v3/documentation/network/protocols/rldp)
- [TON DHT Сервис](/v3/documentation/network/protocols/dht/ton-dht)
