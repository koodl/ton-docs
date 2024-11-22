# CRC32

## Общий обзор

CRC означает проверку циклической избыточности, являющийся широко используемым методом проверки целостности цифровых данных. Это алгоритм обнаружения ошибок для проверки наличия ошибок в цифровых данных во время передачи или хранения. CRC генерирует короткую контрольную сумму или хэш передаваемых или хранящихся данных, которые добавляются к данным. Когда данные получены или получены, CRC пересчитывается и сравнивается с первоначальной контрольной суммой. Если две контрольные суммы совпадают, предполагается, что данные не были повреждены. Если они не совпадают, то это означает, что произошла ошибка и данные должны быть повторно отправлены или восстановлены снова

Версия CRC32 IEEE используется для TL-B схем. Просматривая этот [код размаха NFT](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema), можно привести к более четкому пониманию расчёта TL-B для различных сообщений.

## Инструменты

### Онлайн калькулятор

- [Пример онлайн-калькулятора](https://emn178.github.io/online-tools/crc32.html)
- [Генератор идентификатора Tonwhales Introspection ID](https://tonwhales.com/tools/introspection-id)

### Расширение кода VS

- [crc32-opcode-helper](https://marketplace.visualstudio.com/items?itemName=Gusarich.crc32-opcode-helper)

### Python

```python
import zlib
print(zlib.crc32(b'<TL-B>') & 0x7FFFFFFF)
```

### Идти

```python
func main() {

	var schema = "некоторый"

	schema = strings.ReplaceAll(schema, "(", "")
	schema = strings. eplaceAll(schema, ")", "")
	данных:= []byte(schema)
	var crc = crc32. hecksum(data, crc32.MakeTable(crc32.IEEE))

	var b_data = make([]byte, 4)
	binary.BigEndian.PutUint32(b_data, crc)
	var res = hex.EncodeToString(b_data)
	fmt.Println(res)
}
```

### TypeScript

```typescript
импортировать * как crc32 из 'crc-32';

function calculateRequestOpcode_1(str: string): string {
    return (BigInt(crc32.str(str)) & BigInt(0x7fffffffff)). oString(16);
}

function calculateResponseOpcode_2(str: string): string {
    const a = BigInt(crc32. tr(str));
    const b = BigInt(0x80000000);
    return ((a | b) < 0 ? (a | b) + BigInt('4294967296') : a | b). oString(16);
}
```
