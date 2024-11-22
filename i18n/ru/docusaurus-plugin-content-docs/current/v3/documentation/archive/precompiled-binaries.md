импортировать вкладки из '@theme/Tabs';
импортировать вкладки из '@theme/TabItem';
импортировать кнопку из '@site/src/components/button'

# Прекомпилированные файлы

:::caution важно
Вам больше не нужно вручную устанавливать бинарные файлы с помощью Blueprint SDK.
:::

Все бинарные файлы для разработки и тестирования снабжены программой Blueprint SDK.

<Button href="/v3/documentation/smart-contracts/getting-started/javascript"
colorType="primary" sizeType={'sm'}>

Мигрировать в Чертеж SDK

</Button>

## Прекомпилированные файлы

Если вы не используете Blueprint SDK для разработки смарт-контрактов, вы можете использовать предварительно скомпилированные файлы для вашей операционной системы и выбранного инструмента.

### Предпосылки

Для локальной разработки смарт-контрактов TON _без Javascript_, вам нужно подготовить бинарные файлы `func`, `fift` и `lite client` на вашем устройстве.

Вы можете скачать и настроить их ниже, или прочитать эту статью из TON Society:

- [Настройка среды разработки TON](https://blog.ton.org/setting-up-a-ton-development-environment)

### 1. Скачать

Загрузите файлы из таблицы ниже.  Убедитесь, что вы выбрали правильную версию для вашей операционной системы и установите любые дополнительные зависимости:

| ОС                                 | TON файлы                                                                                       | фифт                                                                                         | func                                                                                         | лито-клиент                                                                                         | Дополнительные зависимости                                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| MacOS x86-64                       | [download](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-x86-64.zip)   | [download](https://github.com/ton-blockchain/ton/releases/latest/download/fift-mac-x86-64)   | [download](https://github.com/ton-blockchain/ton/releases/latest/download/func-mac-x86-64)   | [download](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-mac-x86-64)   |                                                                                                                 |
| MacOS arm64                        | [download](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-arm64.zip)    |                                                                                              |                                                                                              |                                                                                                     | `brew install openssl ninja libmicrohttpd pkg-config`                                                           |
| Windows x86-64                     | [download](https://github.com/ton-blockchain/ton/releases/latest/download/ton-win-x86-64.zip)   | [download](https://github.com/ton-blockchain/ton/releases/latest/download/fift.exe)          | [download](https://github.com/ton-blockchain/ton/releases/latest/download/func.exe)          | [download](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client.exe)          | Установить [OpenSSL 1.1.1](/ton-binaries/windows/Win64OpenSSL_Light-1_1_1q.msi) |
| Linux  x86_64 | [download](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-x86_64.zip) | [download](https://github.com/ton-blockchain/ton/releases/latest/download/fift-linux-x86_64) | [download](https://github.com/ton-blockchain/ton/releases/latest/download/func-linux-x86_64) | [download](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-linux-x86_64) |                                                                                                                 |
| Linux arm64                        | [download](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-arm64.zip)  |                                                                                              |                                                                                              |                                                                                                     | `sudo apt установите libatomic1 libssl-dev`                                                                     |

### 2. Настройка бинарных файлов

export const Highlight = ({children, color}) => (
<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#fff',
padding: '0.2rem',
}}>
{children} </span>
);

<Tabs groupId="operating-systems">
  <TabItem value="win" label="Windows">

1. После загрузки вам нужно `create` новую папку. Например: **`C:/Users/%USERNAME%/ton/bin`** и переместите там установленные файлы.

2. Чтобы открыть переменные окружения Windows, нажмите кнопки <Highlight color="#1877F2">Win + R</Highlight> на клавиатуре, введите `sysdm.cpl` и нажмите Enter.

3. На вкладке "_Advanced_" нажмите кнопку <Highlight color="#1877F2">"Environment Variables..."</Highlight>.

4. В разделе _"User variables"_ выберите переменную "_Path_" и нажмите <Highlight color="#1877F2">"Edit"</Highlight> (это обычно требуется).

5. Чтобы добавить новое значение `(путь)` в системную переменную в следующем окне, нажмите кнопку <Highlight color="#1877F2">"Новая"</Highlight>.
   В новом поле необходимо указать путь к папке, в которой хранятся ранее установленные файлы:

```
C:\Users\%USERNAME%\tв\bin\
```

6. Чтобы проверить, правильно ли все было установлено, запустите в терминале (_cmd.exe_):

```bash
fift -V - и func -V - и lite-клиент -V
```

7. Если вы планируете использовать пять, вам нужна переменная окружения `FIFTPATH` с необходимым импортом:

   1. Скачать [fiftlib.zip](/ton-binaries/windows/fiftlib.zip)
   2. Откройте архив в некоторых каталогах на вашей машине (например, **`C:/Users/%USERNAME%/ton/lib/fiftlib`**)
   3. Создайте новую (нажмите кнопку <Highlight color="#1877F2">"New"</Highlight>) переменную окружения `FIFTPATH` в разделе "_User variables_".
   4. В поле "_Variable value_" укажите путь к файлам: **`/%USERNAME%/ton/lib/fiftlib`** и нажмите <Highlight color="#1877F2">OK</Highlight>. Готово.

:::caution важно
Вместо `%USERNAME%` ключа `, вы должны вставить свой `username\`.\
:::</TabItem>
<TabItem value="mac" label="Linux / MacOS">1. После загрузки убедитесь, что загруженные файлы исполняются путем изменения их разрешений.```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```2. Также полезно добавить эти файлы в ваш путь (или скопировать их в `/usr/local/bin`), чтобы вы могли получить доступ к ним где угодно.```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```3. Чтобы убедиться, что все было установлено правильно, запустите в терминале.```bash
fift -V && func -V && lite-client -V
```4. Если вы планируете `use fift`, также скачайте [fiftlib.zip](/ton-binaries/windows/fiftlib. В некоторых каталогах на вашем устройстве (например `/usr/local/lib/fiftlib`), откройте zip и установите переменную окружения `FIFTPATH` на эту директорию.```
unzip fiftlib. ip
mkdir -p /usr/local/lib/fiftlib
cp fiftlib/* /usr/local/lib/fiftlib
```::info Эй, вы почти закончили :)
Не забудьте установить [переменную окружения](https://stackoverflow. om/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH`, чтобы указать на этот каталог.
:::

</TabItem>
<TabItem value="mac" label="Linux / MacOS">

1. После загрузки убедитесь, что загруженные файлы исполняются путем изменения их разрешений.

```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```

2. Также полезно добавить эти файлы в ваш путь (или скопировать их в `/usr/local/bin`), чтобы вы могли получить доступ к ним где угодно.

```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```

3. Чтобы убедиться, что все было установлено правильно, запустите в терминале.

```bash
fift -V && func -V && lite-client -V
```

4. Если вы планируете `use fift`, также скачайте [fiftlib.zip](/ton-binaries/windows/fiftlib. В некоторых каталогах на вашем устройстве (например `/usr/local/lib/fiftlib`), откройте zip и установите переменную окружения `FIFTPATH` на эту директорию.

```
распаковать fiftlib.zip
mkdir -p /usr/local/lib/fiftlib
cp fiftlib/* /usr/local/lib/fiftlib
```

:::info Hey, you're almost finished :)
Remember to set the [environment variable](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH` to point to this directory.
:::

  </TabItem>
</Tabs>

## Собрать из исходного кода

Если вы не хотите полагаться на предварительно скомпилированные бинарные файлы и предпочитаете сами компилировать бинарные файлы, вы можете выполнить [официальные инструкции](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions).

Готовы к использованию гистограммы приведены ниже:

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install git make cmake g++ libssl-dev zlib1g-dev wget
cd ~ && git clone https://github.com/ton-blockchain/ton. it
cd ~/ton && git submodule update --init
mkdir ~/ton/build && cd ~/ton/build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j 4
```

## Другие источники для бинарных файлов

Основная команда предоставляет автоматические сборки для нескольких операционных систем как [GitHub Actions](https://github.com/ton-blockchain/ton/releases/latest).

Нажмите на ссылку выше, выберите рабочий процесс слева от вашей операционной системы, нажмите на недавний зеленый проходящий сборок, и скачайте `ton-binaries` в разделе "Artifacts".
