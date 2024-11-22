# TL-B Tools

## TL-B Parsers

Парсеры TL-B помогают проводить сериализацию основных [типов TL-B](/v3/documentation/data-formats/tlb/tl-b-types). Каждый из которых
реализует типы TL-B в качестве объекта, и возвращает сериализованные бинарные данные.

| Язык       | SDK                                                                                                                  | Соцсети                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Kotlin     | [ton-kotlin](https://github.com/ton-community/ton-kotlin/tree/main/tlb) (+ парсинг файлов `.tlb`) | https://t.me/tonkotlin                      |
| Идти       | [tonutils](https://github.com/xssnick/tonutils-go/tree/master/tlb)                                                   | https://t.me/tonutils                       |
| Идти       | [tongo](https://github.com/tonkeeper/tongo/tree/master/tlb) (+ парсинг файлов `.tlb`)             | https://t.me/tongo_lib |
| TypeScript | [tlb-parser](https://github.com/ton-community/tlb-parser)                                                            | -                                                                           |
| Python     | [ton-kotlin](https://github.com/disintar/tonpy) (+ разбор файлов `.tlb`)                          | https://t.me/dtontech                       |

## TL-B Generator

[tlb-codegen](https://github.com/ton-community/tlb-codegen) пакет позволяет генерировать код Typescript для сериализации и десериализации структур в соответствии с предусмотренной схемой TLB.

[tonpy](https://github.com/disintar/tonpy) пакет позволяет генерировать код Python для сериализации и десериализации структур в соответствии со схемой TLB.
