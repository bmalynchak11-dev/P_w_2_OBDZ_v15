"""Відкриті тести задачі 6: Атрибути, що порушують 2NF і 3NF.

Запуск: pytest tests/test_variant_06.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import pytest
from conftest import load
from helpers import *  # noqa: F401,F403


CASES = [
    ("S1", (ATTRS_1, FDS_1), {"2NF": S("order_date customer_id customer_name product_name price"),
                              "3NF": S("order_date customer_id customer_name product_name price")}),
    ("S1", (S("A B C D E"), F("A -> B C; D -> E")), {"2NF": S("B C E"), "3NF": S("B C E")}),
    ("S2", (ATTRS_2, FDS_2), {"2NF": S(), "3NF": S()}),
    ("S2", (S("A B C"), F("A B -> C; C -> B")), {"2NF": S(), "3NF": S()}),
    ("S3", (ATTRS_3, FDS_3), {"2NF": S(), "3NF": S("patient_name doctor_name department")}),
    ("S3", (S("A B C D"), F("A -> B; B -> C; C -> D")), {"2NF": S(), "3NF": S("C D")}),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_nf_violations(case):
    check(load(6).nf_violations, case[1], case[2])
