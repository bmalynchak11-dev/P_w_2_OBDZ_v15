"""Відкриті тести задачі 1: Замикання множини атрибутів.

Запуск: pytest tests/test_variant_01.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403


CASES = [
    ("S1", (S("order_id"), FDS_1), S("order_id order_date customer_id customer_name")),
    ("S1", (S("order_id product_id"), FDS_1), ATTRS_1),
    ("S2", (S("teacher"), FDS_2), S("teacher subject")),
    ("S2", (S("student teacher"), FDS_2), ATTRS_2),
    ("S3", (S("doctor_id"), FDS_3), S("doctor_id doctor_name department")),
    ("S3", (S("visit_id"), FDS_3), ATTRS_3),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_closure(case):
    check(load(1).closure, case[1], case[2])
