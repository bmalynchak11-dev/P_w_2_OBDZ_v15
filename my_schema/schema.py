"""Моя схема: атрибути, залежності, ключі, нормальна форма й декомпозиція (розділ 9 завдання).

Заповніть п'ять змінних внизу. Перевірка: python check_my_schema.py N (N - номер вашого набору 1..3).
"""


def S(text=""):
    """S("a b c") -> frozenset({"a", "b", "c"})."""
    return frozenset(text.split())


def F(text=""):
    """F("a b -> c; c -> d") -> список пар (frozenset, frozenset)."""
    result = []
    for part in text.split(";"):
        if part.strip():
            left, right = part.split("->")
            result.append((S(left), S(right)))
    return result


ATTRS = S("")        # ЗАПОВНІТЬ: усі стовпці таблиці вашого набору
FDS = F("")          # ЗАПОВНІТЬ: функціональні залежності предметної області
KEYS = set()         # ЗАПОВНІТЬ: множина ключів-кандидатів, кожен ключ - frozenset, наприклад {S("a b")}
NORMAL_FORM = ""     # ЗАПОВНІТЬ: "1NF", "2NF", "3NF" або "BCNF"
PARTS = []           # ЗАПОВНІТЬ: декомпозиція у 3NF: список відношень, кожне - frozenset
