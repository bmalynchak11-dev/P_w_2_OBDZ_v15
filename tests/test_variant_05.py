"""Відкриті тести задачі 5: Нормальна форма схеми.

Запуск: pytest tests/test_variant_05.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403


CASES = [
    ("S1", (ATTRS_1, FDS_1), "1NF"),
    ("S1", (S("A B C"), F("A -> B C")), "BCNF"),
    ("S2", (ATTRS_2, FDS_2), "3NF"),
    ("S2", (S("A B C"), F("A B -> C; C -> B")), "3NF"),
    ("S3", (ATTRS_3, FDS_3), "2NF"),
    ("S3", (S("A B C"), F("A -> B; B -> C")), "2NF"),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_normal_form(case):
    check(load(5).normal_form, case[1], case[2])
