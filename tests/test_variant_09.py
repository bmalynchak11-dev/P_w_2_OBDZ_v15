"""Відкриті тести задачі 9: Декомпозиція без втрат.

Запуск: pytest tests/test_variant_09.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

PARTS_3 = [S("visit_id patient_id doctor_id diagnosis"), S("patient_id patient_name"),
           S("doctor_id doctor_name department")]


CASES = [
    ("S1", (ATTRS_1, FDS_1, [S("order_id order_date customer_id customer_name"),
                             S("order_id product_id product_name price qty")]), True),
    ("S1", (ATTRS_1, FDS_1, [S("order_id order_date customer_id"),
                             S("customer_id customer_name product_id product_name price qty")]), False),
    ("S2", (ATTRS_2, FDS_2, [S("teacher subject"), S("student teacher grade")]), True),
    ("S2", (ATTRS_2, FDS_2, [S("student subject"), S("subject teacher grade")]), False),
    ("S3", (ATTRS_3, FDS_3, PARTS_3), True),
    ("S3", (ATTRS_3, FDS_3, [S("visit_id patient_id patient_name doctor_id diagnosis"), S("doctor_name department")]), False),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_is_lossless(case):
    check(load(9).is_lossless, case[1], case[2])
