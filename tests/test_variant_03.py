"""Відкриті тести задачі 3: Ключі-кандидати.

Запуск: pytest tests/test_variant_03.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

CLASSIC = F("A B -> C; C D -> E; B -> D; E -> A")


CASES = [
    ("S1", (ATTRS_1, FDS_1), {S("order_id product_id")}),
    ("S1", (S("A B C"), F("")), {S("A B C")}),
    ("S2", (ATTRS_2, FDS_2), {S("student subject"), S("student teacher")}),
    ("S2", (S("A B C"), F("A B -> C; C -> A")), {S("A B"), S("B C")}),
    ("S3", (ATTRS_3, FDS_3), {S("visit_id")}),
    ("S3", (S("A B C D E"), CLASSIC), {S("A B"), S("B C"), S("B E")}),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_candidate_keys(case):
    check(load(3).candidate_keys, case[1], case[2], unordered=True)
