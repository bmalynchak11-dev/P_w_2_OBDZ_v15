"""Відкриті тести задачі 4: Мінімальне покриття.

Запуск: pytest tests/test_variant_04.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

NOISY_1 = FDS_1 + F("order_id -> customer_name; order_id product_id -> order_date; order_id product_id -> product_name")
NOISY_2 = F("student subject -> teacher; teacher -> subject; student subject -> subject; student teacher -> subject")
NOISY_3 = FDS_3 + F("visit_id -> patient_name; visit_id patient_id -> doctor_id; doctor_id -> department doctor_name")


CASES = [
    ("S1", (NOISY_1,), F("order_id -> order_date; order_id -> customer_id; customer_id -> customer_name; "
                          "product_id -> product_name; product_id -> price; order_id product_id -> qty")),
    ("S2", (NOISY_2,), F("student subject -> teacher; teacher -> subject")),
    ("S3", (NOISY_3,), F("visit_id -> patient_id; visit_id -> doctor_id; visit_id -> diagnosis; "
                          "patient_id -> patient_name; doctor_id -> doctor_name; doctor_id -> department")),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_minimal_cover(case):
    check(load(4).minimal_cover, case[1], case[2], unordered=True)
