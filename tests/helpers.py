"""Допоміжні засоби тестів: компактний запис множин і залежностей та три схеми-приклади.

Атрибут: рядок. Множина атрибутів: frozenset. Залежність: пара (lhs, rhs) двох frozenset.
Схема набору 1: замовлення; набору 2: навчання; набору 3: лікарня.
"""
import copy
from collections import Counter

import pytest


def S(text=""):
    """S("a b c") -> frozenset({"a", "b", "c"})."""
    return frozenset(text.split())


def F(text=""):
    """F("a b -> c d; c -> e") -> [(frozenset, frozenset), ...]."""
    result = []
    for part in text.split(";"):
        if part.strip():
            left, right = part.split("->")
            result.append((S(left), S(right)))
    return result


# Набір 1: замовлення
ATTRS_1 = S("order_id order_date customer_id customer_name product_id product_name price qty")
FDS_1 = F("order_id -> order_date customer_id; customer_id -> customer_name; "
          "product_id -> product_name price; order_id product_id -> qty")
# Набір 2: навчання
ATTRS_2 = S("student subject teacher grade")
FDS_2 = F("student subject -> teacher grade; teacher -> subject")
# Набір 3: лікарня
ATTRS_3 = S("visit_id patient_id patient_name doctor_id doctor_name department diagnosis")
FDS_3 = F("visit_id -> patient_id doctor_id diagnosis; patient_id -> patient_name; "
          "doctor_id -> doctor_name department")


def norm(value):
    """Множини порівнюються як множини, списки й кортежі як послідовності."""
    if isinstance(value, (set, frozenset)):
        return frozenset(norm(v) for v in value)
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    return value


def _freeze(value):
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, dict):
        return frozenset((k, _freeze(v)) for k, v in value.items())
    return value


def as_unordered(value):
    """Множина або список без урахування порядку (але з урахуванням повторів)."""
    return frozenset(Counter(_freeze(norm(v)) for v in value).items())


def drop_inner(parts):
    """Прибирає частини, що є підмножинами інших частин (для порівняння декомпозицій)."""
    unique = list(dict.fromkeys(frozenset(p) for p in parts))
    return [p for p in unique if not any(p < q for q in unique)]


def check(function, args, expected, unordered=False, reduce=False):
    """Викликає function(*args) і порівнює з expected (ValueError порівнюється за текстом)."""
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            function(*args)
        assert str(info.value) == str(expected)
    else:
        got = function(*args)
        if reduce:
            got = drop_inner(got)
        if unordered:
            assert as_unordered(got) == as_unordered(expected)
        else:
            assert norm(got) == norm(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"
