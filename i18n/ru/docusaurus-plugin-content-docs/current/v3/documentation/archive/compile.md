# Компилировать и создавать смарт-контракты на TON

Вот список библиотек и репозиториев для создания вашего смарт-контракта.

**TLDR:**

- В большинстве случаев достаточно использовать чертеж SDK.
- Если вам нужен более низкоуровневый подход, вы можете использовать тон-компилятор или func-js.

## Чертеж

### Общий обзор

Окружение для блокчейна TON для написания, тестирования и развертывания смарт-контрактов. Подробнее в [git repository](https://github.com/ton-community/blueprint).

### Установка

Выполните следующие действия в терминале для создания нового проекта и следуйте инструкциям на экране:

```bash
npm создать ton@latest
```

&nbsp;

### Возможности

- Упорядоченный рабочий процесс для разработки, тестирования и развертывания смарт-контрактов
- Мертвая простая установка в mainnet/testnet с помощью вашего любимого кошелька (например, Tonkeeper)
- Блэк быстрое тестирование нескольких смарт-контрактов в изолированном блокчейне, запущенном в процессе

### Технический стек

1. Компиляция FunC с помощью https://github.com/ton-community/func-js (без CLI)
2. Тестирование смарт-контрактов с https://github.com/ton-community/sandbox
3. Развертывание смарт-контрактов с [TON Connect 2](https://github.com/ton-connect), [Wallet](https://tonhub.com/) или `ton://` глубже

### Требования

- [Node.js](https://nodejs.org) с последней версией, например v18, проверьте версию с помощью `node -v`
- IDE с поддержкой TypeScript и FunC, например, [код Visual Studio](https://code.visualstudio.com/) с [плагином FunC](https://marketplace.visualstudio.com/items?itemName=tonwhales.func-vscode)

### Как использовать?

- [Смотреть презентацию DoraHacks с демонстрацией работы с чертежами](https://www.youtube.com/watch?v=5ROXVM-Fojo).
- Читайте подробное описание в [Репозиции чертеже](https://github.com/ton-community/blueprint#create-a-new-project).

## тонн-компилятор

### Общий обзор

Упакованный компилятор FunC для смарт-контрактов TON:

- GitHub: [ton-community/ton-compiler](https://github.com/ton-community/ton-compiler)
- NPM: [ton-compiler](https://www.npmjs.com/package/ton-compiler)

### Установка

```bash npm2yarn
npm install ton-compiler
```

### Возможности

- Несколько версий компилятора FunC
- Не нужно устанавливать и компилировать TON
- Интерфейсы программирования и CLI
- Готов к использованию в модульном тестировании

### Как использовать

Это пакеты добавляют в проект двоичный файл `ton-compiler`.

Сборка FunC - это многоступенчатый процесс. Один из них компилирует Func в Fift код, который затем компилируется в бинарное представление. Fift компилятор уже имеет Asm.fif комплект.

FunC stdlib в комплекте, но может быть отключён при запуске.

#### Использование консоли

```bash
# Компилировать в бинарную форму (для создания контракта)
ton-compiler --input ./wallet.fc --output . wallet.cell

# Компилировать до конца (полезно для отладки)
тон-компилятор --input . wallet.fc --output-fift ./wallet.fif

# Компилировать в бинарную форму и fift
ton-compiler --input ./wallet. c --output ./wallet.cell --output-fift ./wallet.fif

# Отключить stdlib
ton-compiler --no-stdlib --input ./wallet.fc --output ./wallet. ell --output-fift ./wallet.fif

# Выберите версию
ton-compiler --version "legacy" --input ./wallet.fc --output ./wallet.cell --output-fift ./wallet.fif
```

#### Программное использование

```javascript
import { compileContract } from "ton-compiler";
let result = await compileContract({ code: 'source code', stdlib: true, version: 'latest' });
if (result.ok) {
  console.log(result. ift); // Compiled Fift assembler
  console.log(result. ell); // Скомпилированная ячейка буфер
} else {
  console.warn(result.logs); // Выходные логи
}
```

## func-js

### Общий обзор

_Cross-platform_ для компилятора TON FunC.

Это более низкий уровень, чем тон-компилятор, поэтому используйте его только в том случае, если для вас не работает тон-компилятор.

- GitHub: [ton-community/func-js](https://github.com/ton-community/func-js)
- NPM: [@ton-community/func-js](https://www.npmjs.com/package/@ton-community/func-js)

### Установка

```bash npm2yarn
npm install @ton-community/func-js
```

### Возможности

- Не нужно компилировать файлы загрузки FunC
- Работает в Node.js и **WEB** (WASM поддержка)
- Собирает прямо в BOC с помощью ячейки кода
- Сборка возвращена в целях отладки
- Не зависит от файловой системы

### Как использовать

Во внутреннем плане этот пакет использует оба интерпретатора FunC компилятора и Fift вместе с одной lib, скомпилированной в WASM.

Простая схема:

```bash
(ваш код) -> WASM(FunC -> Fift -> BOC)
```

Источники внутренней библиотеки можно найти [here](https://github.com/ton-blockchain/ton/tree/testnet/crypto/funcfiftlib).

### Пример использования

```javascript
импортировать {compileFunc, compilerVersion} из '@ton-community/func-js';
импортировать {Cell} из 'ton';

async function main() {
    // Вы можете загрузить версию компилятора 
    с помощью версии = await compilerVersion();
    
    let result = await compileFunc({
        // Entry points of your project
        entryPoints: ['main. c'],
        // Источники
        источников: {
            "stdlib. c": "<stdlibCode>",
            "main". c": "<contractCode>",
            // Остаток файлов, которые включены в основную. c if some
        }
    });

    если (результат. tatus === 'error') {
        console.error(result. essage)
        return;
    }

    // результат. odeBoc содержит BOC с кодовым ячейкой 
    пустой codeCell = CЯ. romBoc(Buffer.from(result.codeBoc, "base64"))[0];
    
    // результат. iftCode содержит сборочную версию вашего кода (для целей отладки)
    console.log(result.fiftCode)
}
```

Обратите внимание, что все содержимое исходных файлов FunC, используемых в вашем проекте, должно быть передано в `sources`, включая:

- точки входа
- stdlib.fc (если вы используете его)
- все файлы, включенные в точки входа

### Проверено сообществом TON

- [ton-community/ton-compiler](https://github.com/ton-community/ton-compiler) — готовый к использованию компилятор для смарт-контрактов TON.
- [ton-community/func-js](https://github.com/ton-community/func-js) — кросс-платформенные привязки для компилятора FunC TON.

### Сторонние участники

- [grozzzny/ton-compiler-groz](https://github.com/grozzzny/ton-compiler-groz) — компилятор для смарт-контрактов TON FunC.
- [Termina1/tonc](https://github.com/Termina1/tonc) — TONC (TON Compiler). Использует WASM, так идеально подходит для Linux.

## Прочие вопросы

- [disintar/toncli](https://github.com/disintar/toncli) — один из самых популярных подходов. Вы даже можете использовать его с Docker.
- [tonthemoon/ton](https://github.com/tonthemoon/ton) — _(closed beta)_ установщик двоичных файлов TON.
- [delab-team/tlbcrc](https://github.com/delab-team/tlbcrc) — Пакет и CLI, чтобы сгенерировать opcodes по схеме TL-B
