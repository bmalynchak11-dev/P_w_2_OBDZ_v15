"""Відкриті тести задачі 8: Декомпозиція у BCNF.

Запуск: pytest tests/test_variant_08.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403


CASES = [
    ("S1", (S("order_id customer_id customer_name"), F("order_id -> customer_id; customer_id -> customer_name")), [S("customer_id customer_name"), S("order_id customer_id")]),
    ("S2", (ATTRS_2, FDS_2), [S("teacher subject"), S("student teacher grade")]),
    ("S2", (S("A B C"), F("A B -> C; C -> B")), [S("C B"), S("A C")]),
    ("S3", (S("visit_id doctor_id doctor_name department"), F("visit_id -> doctor_id; doctor_id -> doctor_name department")), [S("doctor_id doctor_name department"), S("visit_id doctor_id")]),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_decompose_bcnf(case):
    check(load(8).decompose_bcnf, case[1], case[2], unordered=True, reduce=True)
