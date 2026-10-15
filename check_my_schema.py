"""Перевірка власної схеми студента: python check_my_schema.py N  (N = 1, 2, 3 - номер набору).
Для частини Б (таблиця з вашого дипломного проєкту): python check_my_schema.py own my_schema/diploma_schema.py my_schema/diploma_table.csv

Скрипт перевіряє структуру й узгодженість з прикладом даних data/own_domain_N.csv:
чи кожна ваша залежність виконується в таблиці, чи ключі не повторюються, чи частини декомпозиції
покривають усі стовпці й чи з'єднання проєкцій відновлює таблицю без зайвих рядків.
Скрипт не перевіряє, чи знайдено всі залежності, ключі та нормальну форму: це перевіряє викладач.
"""
import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORMS = ("1NF", "2NF", "3NF", "BCNF")


def load_schema(path):
    spec = importlib.util.spec_from_file_location("my_schema_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_rows(number):
    """number: номер набору 1..3 або шлях до власного файла CSV (частина Б)."""
    path = ROOT / "data" / f"own_domain_{number}.csv" if isinstance(number, int) else Path(number)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames), list(reader)


def join_parts(rows, parts):
    """Природне з'єднання проєкцій; повертає множину кортежів у порядку відсортованих атрибутів."""
    joined = [dict()]
    for part in parts:
        projection = {tuple(sorted((a, row[a]) for a in part)) for row in rows}
        merged = []
        for left in joined:
            for item in projection:
                item = dict(item)
                if all(left.get(a, item[a]) == item[a] for a in item):
                    merged.append({**left, **item})
        joined = merged
    return {tuple(sorted(row.items())) for row in joined}


def check(module, number):
    problems = []
    header, rows = read_rows(number)
    attrs = frozenset(header)
    if frozenset(getattr(module, "ATTRS", ())) != attrs:
        problems.append(f"ATTRS має збігатися зі стовпцями таблиці: {sorted(attrs)}")
        return problems
    fds = list(getattr(module, "FDS", []))
    if not fds:
        problems.append("FDS порожній: запишіть залежності")
    for index, pair in enumerate(fds, start=1):
        try:
            lhs, rhs = (frozenset(x) for x in pair)
        except (TypeError, ValueError):
            problems.append(f"залежність {index}: очікується пара (lhs, rhs) з множин атрибутів")
            continue
        if not lhs or not rhs:
            problems.append(f"залежність {index}: порожня частина")
        elif not (lhs | rhs) <= attrs:
            problems.append(f"залежність {index}: невідомі атрибути {sorted((lhs | rhs) - attrs)}")
        elif rhs <= lhs:
            problems.append(f"залежність {index}: тривіальна (права частина міститься в лівій)")
        else:
            seen = {}
            for row in rows:
                left = tuple(row[a] for a in sorted(lhs))
                right = tuple(row[a] for a in sorted(rhs))
                if seen.setdefault(left, right) != right:
                    problems.append(f"залежність {index} ({sorted(lhs)} -> {sorted(rhs)}) порушена в таблиці")
                    break
    keys = list(getattr(module, "KEYS", []))
    if not keys:
        problems.append("KEYS порожній: має бути хоча б один ключ-кандидат")
    keys = [frozenset(k) for k in keys]
    for key in keys:
        if not key or not key <= attrs:
            problems.append(f"ключ {sorted(key)} порожній або містить невідомі атрибути")
        elif len({tuple(row[a] for a in sorted(key)) for row in rows}) != len(rows):
            problems.append(f"ключ {sorted(key)}: у таблиці є рядки з однаковим значенням ключа")
    for a in keys:
        for b in keys:
            if a < b:
                problems.append(f"ключ {sorted(b)} не мінімальний: містить ключ {sorted(a)}")
    if getattr(module, "NORMAL_FORM", None) not in FORMS:
        problems.append(f"NORMAL_FORM має бути одним із {FORMS}")
    parts = [frozenset(p) for p in getattr(module, "PARTS", [])]
    if len(parts) < 2:
        problems.append("PARTS: потрібна декомпозиція щонайменше на два відношення")
    else:
        if any(not p <= attrs for p in parts) or frozenset().union(*parts) != attrs:
            problems.append("PARTS: відношення мають покривати рівно всі стовпці таблиці")
        elif any(a < b for a in parts for b in parts):
            problems.append("PARTS: одне відношення міститься в іншому")
        else:
            original = {tuple(sorted(row.items())) for row in rows}
            if join_parts(rows, parts) != original:
                problems.append("PARTS: з'єднання проєкцій дає інші рядки, ніж таблиця (декомпозиція з втратами)")
    return problems


def main(argv):
    if len(argv) == 4 and argv[1] == "own":
        path, source = Path(argv[2]), Path(argv[3])
        if not source.is_file():
            print(f"Немає файла з даними {source}")
            return 2
    elif len(argv) >= 2 and argv[1] in ("1", "2", "3"):
        path = Path(argv[2]) if len(argv) > 2 else ROOT / "my_schema" / "schema.py"
        source = int(argv[1])
    else:
        print(__doc__)
        return 2
    problems = check(load_schema(path), source)
    if problems:
        print("Зауваження:")
        for item in problems:
            print(" -", item)
        return 1
    print("Зауважень немає (змістову повноту перевіряє викладач).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
