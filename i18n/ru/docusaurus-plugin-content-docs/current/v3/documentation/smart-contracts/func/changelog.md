# История FunC

# Начальная версия

Первоначальная версия была сделана с помощью Telegram и активное развитие было прекращено после мая 2020 года. Мы называем версию мая 2020 года "initial".

# Версия 0.1.0

Опубликовано в [05.2022 обновление](https://github.com/ton-blockchain/ton/releases/tag/v2022.05).

В этой версии были добавлены:

- [Constants](/v3/documentation/smart-contracts/func/docs/literals_identifiers#constants)
- [Расширенные строковые литералы](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)
- [Праги семверов](/v3/documentation/smart-contracts/func/docs/compiler_directives#pragma-version)
- [Includes](/v3/documentation/smart-contracts/func/docs/compiler_directives#pragma-version)

Исправлено:

- Исправлены редкие ошибки в Asm.fif.

# Версия 0.2.0

Опубликовано в [08.2022 обновление](https://github.com/ton-blockchain/ton/releases/tag/v2022.08).

В этой версии были добавлены:

- Несбалансированные/другие ветки (когда некоторые ветки вернулись, а некоторые нет)

Исправлено:

- [FunC неправильно обрабатывает циклы «while(false) #377](https://github.com/ton-blockchain/ton/issues/377)
- [FunC incorreclty генерирует код для других ветвей #374](https://github.com/ton-blockchain/ton/issues/374)
- [Функция неправильно возвращается из состояния функции inline #370](https://github.com/ton-blockchain/ton/issues/370)
- [Asm.fif: неправильное разделение больших тел функции помешало строкам #375](https://github.com/ton-blockchain/ton/issues/375)

# Версия 0.3.0

Опубликовано в [10.2022 обновление](https://github.com/ton-blockchain/ton/releases/tag/v2022.10).

В этой версии были добавлены:

- [Мультистрочные асмы](/v3/documentation/smart-contracts/func/docs/functions#multiline-asms)
- Разрешено дублирование одинакового определения констант и злов
- Разрешены Bitwise операции для констант

# Версия 0.4.0

Выпущено в [01.2023 обновление](https://github.com/ton-blockchain/ton/releases/tag/v2023.01).

В этой версии были добавлены:

- [try/catch statements](/v3/documentation/smart-contracts/func/docs/statements#try-catch-statements)
- [throw_arg функции](/v3/documentation/smart-contracts/func/docs/builtins#throwing-exceptions)
- разрешена модификация на месте и массовые назначения глобальных переменных: `a~inc()` и `(a, b) = (3, 5)`, где `a` является глобальным

Исправлено:

- запрещена неоднозначная модификация локальных переменных после их использования в том же выражении: `var x = (ds, ds~load_uint(32), ds~load_unit(64)); запрещены, в то время как `var x = (ds~load_uint(32), ds~load_unit(64), ds);\` не
- Разрешены пустые встроенные функции
- исправляйте ошибки оптимизации `while`
