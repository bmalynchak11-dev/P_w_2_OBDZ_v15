"""Відкриті тести задачі 2: Перевірка залежності на екземплярі даних.

Запуск: pytest tests/test_variant_02.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

H1 = ("order_id", "customer_id", "customer_name")
R1 = [(1, 10, "Іваненко"), (2, 10, "Іваненко П."), (3, 11, "Коваль"), (4, 10, "Іваненко")]
H2 = ("student", "subject", "teacher")
R2 = [("Коваль", "БД", "Мельник"), ("Шевчук", "БД", "Мельник"), ("Коваль", "БД", "Гончар"),
      ("Бондар", "ОС", "Гончар"), ("Шевчук", "ОС", "Мельник")]
H3 = ("patient_id", "patient_name", "doctor_id", "diagnosis")
R3 = [(1, "Павленко", 7, "J00"), (2, "Савчук", 7, "J00"), (1, "Павленко", 8, "K29"),
      (3, "Мороз", 8, "K29"), (2, "Савчук", 7, "I10")]


CASES = [
    ("S1", (H1, R1, ("customer_id",), ("customer_name",)), [(0, 1), (1, 3)]),
    ("S1", (H1, R1, ("order_id",), ("customer_id",)), []),
    ("S2", (H2, R2, ("teacher",), ("subject",)), [(0, 4), (1, 4), (2, 3)]),
    ("S2", (H2, R2, ("student", "subject"), ("teacher",)), [(0, 2)]),
    ("S3", (H3, R3, ("doctor_id",), ("diagnosis",)), [(0, 4), (1, 4)]),
    ("S3", (H3, R3, ("patient_id", "doctor_id"), ("diagnosis",)), [(1, 4)]),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_fd_violations(case):
    check(load(2).fd_violations, case[1], case[2])
