импортировать аргпарс
импортировать csv
импортировать повторно
Импортировать sys

parser = argparse.ArgumentParser(description="Генерировать справочный документ TVM")
parser.add_argument("instructions_csv", type=str, help="csv файл с инструкциями")
parser.add_argument("doc_template", type=str, help="шаблон для документа")
parser.add_argument("out_file", type=str, help="output file")
args = parser.parse_args()

TABLE_HEADER = \
        "| xxxxxxx<br>Opcode " +\
        "| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br>Fift syntax " +\
        "| xxxxxxxxxxxxxxxxx<br>Стек " +\
        "| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br>Описание " +\
        "| xxxx<br>Газ |\n" +\
        "|:-|:-|:-|:-|:-|"

категории = dict()
cmd_to_name = dict()

с open(args.instructions_csv, "r") как f:
    читатель = csv.DictReader(f)
    для строки в читателе:
        cat = строка ["doc_category"]
        если кот не в категориях:
            категории[cat] = []
        категории[cat].append(строка)
        если строка["name"] != "":
            для s в строке["doc_fift"].split("\n"):
                s = s.strip()
                если с != "":
                    s = s.split()[-1]
                    если s не в cmd_to_name:
                        cmd_to_name[s] = row["name"]

def имя_к идентификаторам(ам):
    return "instr-" + s.lower().replace("_", "-").replace("#", "SHARP")

def make_link(текст, cmd):
    если cmd не в cmd_to_name:
        текст возврата
    имя = cmd_to_name[cmd]
    return "[%s](#%s)" % (текст, имя to_id(имя))

def gen_links(текст):
    return re.sub("`([^ `][^`]* )?([A-Z0-9#-]+)`", lambda m: make_link(m.group(0), m.group(2)), текст)

def make_table(кат):
    если кот не в категориях:
        print("Нет такой категории", кат, file=sys.stderr)
        вернуть ""
    Таблица = [TABLE_HEADER]
    для строки в категориях[cat]:
        opcode = строка ["doc_opcode"]
        fift = строка ["doc_fift"]
        стек = строка ["doc_stack"]
        desc = строка ["doc_description"]
        газ = строка ["doc_gas"]

        если opcode != "":
            opcode = "**`%s`**" % opcode

        if fift != "":
            fift = "<br>".join("`%s`" % s.strip() для s в fift.split("\n"))

        если стек != "":
            стек = "_"%s`_" % стек
            стек = stack.replace("|", "\\|")
            стек = stack.strip()

        desc = desc.replace("|", "\\|")
        desc = desc.replace("\n", "<br>")

        если газ != "":
            газ = gas.replace("|", "\\|")
            газ = "`" + газ + "`"

        desc = gen_links(desc)
        desc = "<div id='%s'>" % name_to_id(строка ["имя"]) + описание

        table.append("| %s | %s | %s | %s | %s |" % (opcode, fift, stack, desc, gas))

    return "\n".join(table)

templ = open(args.doc_template, "r").read()

templ = gen_links(templ)

doc = re.sub("{{ *Table: *([a-zA-Z0-9_-]+) *}}", lambda m: make_table(m.group(1)), templ)
с open(args.out_file, "w") как f:
    print(doc, file=f)
