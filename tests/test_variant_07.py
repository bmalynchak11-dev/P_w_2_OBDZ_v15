"""Відкриті тести задачі 7: Декомпозиція у 3NF.

Запуск: pytest tests/test_variant_07.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

ATTRS_2B = S("student group curator")
FDS_2B = F("student -> group; group -> curator")
PARTS_1 = [S("order_id order_date customer_id"), S("customer_id customer_name"),
           S("product_id product_name price"), S("order_id product_id qty")]
PARTS_3 = [S("visit_id patient_id doctor_id diagnosis"), S("patient_id patient_name"),
           S("doctor_id doctor_name department")]


CASES = [
    ("S1", (ATTRS_1, FDS_1), PARTS_1),
    ("S2", (ATTRS_2B, FDS_2B), [S("student group"), S("group curator")]),
    ("S3", (ATTRS_3, FDS_3), PARTS_3),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_decompose_3nf(case):
    check(load(7).decompose_3nf, case[1], case[2], unordered=True)
