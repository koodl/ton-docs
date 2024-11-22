# Fift and TVM assembly

Fift is stack-based programming language that has TON-specific features and therefore can work with cells. TVM assembly is also a stack-based programming language, also specific to TON, and it also can work with cells. So what's the difference between them?

## The difference

Fift is executed **at compile-time** - when your compiler builds smart-contract code BOC, after FunC code is processed. Fift can look differently:

```
// tuple primitives
x{6F0} @Defop(4u) TUPLE
x{6F00} @Defop NIL
x{6F01} @Defop SINGLE
x{6F02} dup @Defop PAIR @Defop CONS
```

> TVM opcode definitions in Asm.fif

```
"Asm.fif" include
<{ SETCP0 DUP IFNOTRET // return if recv_internal
   DUP 85143 INT EQUAL OVER 78748 INT EQUAL OR IFJMP:<{ // "seqno" and "get_public_key" get-methods
     1 INT AND c4 PUSHCTR CTOS 32 LDU 32 LDU NIP 256 PLDU CONDSEL  // cnt or pubk
   }>
   INC 32 THROWIF	// fail unless recv_external
   9 PUSHPOW2 LDSLICEX DUP 32 LDU 32 LDU 32 LDU 	//  signature in_msg subwallet_id valid_until msg_seqno cs
   NOW s1 s3 XCHG LEQ 35 THROWIF	//  signature in_msg subwallet_id cs msg_seqno
   c4 PUSH CTOS 32 LDU 32 LDU 256 LDU ENDS	//  signature in_msg subwallet_id cs msg_seqno stored_seqno stored_subwallet public_key
   s3 s2 XCPU EQUAL 33 THROWIFNOT	//  signature in_msg subwallet_id cs public_key stored_seqno stored_subwallet
   s4 s4 XCPU EQUAL 34 THROWIFNOT	//  signature in_msg stored_subwallet cs public_key stored_seqno
   s0 s4 XCHG HASHSU	//  signature stored_seqno stored_subwallet cs public_key msg_hash
   s0 s5 s5 XC2PU	//  public_key stored_seqno stored_subwallet cs msg_hash signature public_key
   CHKSIGNU 35 THROWIFNOT	//  public_key stored_seqno stored_subwallet cs
   ACCEPT
   WHILE:<{
     DUP SREFS	//  public_key stored_seqno stored_subwallet cs _51
   }>DO<{	//  public_key stored_seqno stored_subwallet cs
     8 LDU LDREF s0 s2 XCHG	//  public_key stored_seqno stored_subwallet cs _56 mode
     SENDRAWMSG
   }>	//  public_key stored_seqno stored_subwallet cs
   ENDS SWAP INC	//  public_key stored_subwallet seqno'
   NEWC 32 STU 32 STU 256 STU ENDC c4 POP
}>c
```

> wallet_v3_r2.fif

Последний фрагмент кода выглядит как TVM сборка, и большинство из них на самом деле! Как это случилось?

Представьте, что вы говорите с инструктором, говорите ему "и теперь добавляйте команды, делая это и это в конце функции". Ваши команды в конце концов становятся программой стажера. Они обрабатываются дважды - как здесь, опкоды заглавными буквами (SETCP0, DUP и т.д. ) обрабатываются как по Fift, так и по TVM.

Вы можете объяснить абстракции высокого уровня вашему обучающему, в конечном итоге он будет понимать и уметь их использовать. Fift также расширяется - вы можете определить свои собственные команды. In fact, Asm[Tests].fif is all about defining TVM opcodes.

С другой стороны, ТВМ опкоды выполняются **во время запуска** - это код смарт-контрактов. Они могут быть задуманы как программа Вашего стажера - сборка ТВМ может сделать меньше (напр. он не имеет встроенных примитивов для подписи данных, потому что все, что TVM делает в блокчейне, публично), но он действительно может взаимодействовать со своей средой.

## Использование в смарт-контрактах

### [Fift] - Putting big BOC into contract

Это возможно, если вы используете `toncli`. Если вы используете другие компиляторы, то есть другие способы включить big BOC.
Редактируйте `project.yaml` так, чтобы `fift/blob.fif` был включен при создании кода smart-contract:

```
контракт:
  fift:
    - fift/blob.fif
  функция:
    - func/code.fc
```

Поместите BOC в `fift/blob.boc`, затем добавьте следующий код в `fift/blob.fif`:

```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

Теперь вы можете извлечь этот блок из умного контракта:

```
ячейка load_blob() asm "LDBLOB";

() recv_internal() {
    send_raw_message(load_blob(), 160);
}
```

### [ТВМ сборка] - Преобразование целого в строку

"К сожалению, попытка преобразования внутри строки с использованием примитивов Fift не удалась.

```
срез int_to_string(int x) см "(.) $>s PUSHSLICE";
```

Причина очевидна: Исправление вычисляет время компиляции, где пока нет `x` для конвертации. Для конвертирования непостоянных целых чисел в слой строки требуется сборка TVM. Например, это код одного из участников TON Smart Challenge 3:

```
tuple digitize_number(int value)
  asm "NIL WHILE:<{ OVER }>DO<{ SWAP TEN DIVMOD s1 s2 XCHG TPUSH }> NIP";

строитель_number(builder msg, tuple t)
  asm "WHILE:<{ DUP TLEN }>DO<{ TPOP 48 ADDCONST ROT 8 STU SWAP }> DROP";

builder store_signed(builder msg, int v) inline_ref {
  if (v < 0) {
    return msg. tore_uint(45, 8).store_number(digitize_number(- v));
  } elseif (v == 0) {
    return msg. tore_uint(48, 8);
  } else {
    return msg.store_number(digitize_number(v));
  }
}
```

### [сборка ТВМ] - Дешевое умножение модулей

```
int mul_mod(int a, int b, int m) inline_ref {               ;; 1232 gas units
  (_, int r) = muldivmod(a % m, b % m, m);
  return r;
}
int mul_mod_better(int a, int b, int m) inline_ref {        ;; 1110 gas units
  (_, int r) = muldivmod(a, b, m);
  return r;
}
int mul_mod_best(int a, int b, int m) asm "x{A988} s,";     ;; 65 gas units
```

`x{A988}является опкодом, отформатированным согласно [5.2 Division](/v3/documentation/tvm/instructions#A988): деление с предшествующей умножением, где единственным возвращаемым результатом является третий аргумент модуля. Но opcode должен попасть в smart-contract код - вот что делает `s,\`: он хранит кусочек поверх стека в builder слегка ниже.
