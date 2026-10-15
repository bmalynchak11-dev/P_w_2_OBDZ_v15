"""Відкриті тести задачі 10: Збереження залежностей.

Запуск: pytest tests/test_variant_10.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

PARTS_1 = [S("order_id order_date customer_id"), S("customer_id customer_name"),
           S("product_id product_name price"), S("order_id product_id qty")]
PARTS_3 = [S("visit_id patient_id doctor_id diagnosis"), S("patient_id patient_name"),
           S("doctor_id doctor_name department")]


CASES = [
    ("S1", (ATTRS_1, FDS_1, PARTS_1), True),
    ("S1", (ATTRS_1, FDS_1, [S("order_id order_date customer_id"), S("customer_name product_id product_name price"),
                             S("order_id product_id qty customer_id")]), False),
    ("S2", (ATTRS_2, FDS_2, [S("teacher subject"), S("student teacher grade")]), False),
    ("S2", (ATTRS_2, FDS_2, [S("student subject teacher grade"), S("teacher subject")]), True),
    ("S3", (ATTRS_3, FDS_3, PARTS_3), True),
    ("S3", (ATTRS_3, FDS_3, [S("visit_id patient_id patient_name doctor_id diagnosis"), S("doctor_name department")]), False),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_preserves_dependencies(case):
    check(load(10).preserves_dependencies, case[1], case[2])
