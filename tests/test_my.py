import pytest
from conftest import load
from helpers import S, F, check

M = load(5)  # Задача 5


@pytest.mark.parametrize(
    "args, expected",
    [
        # Тест 1: Схема 1NF через часткову залежність від частини складеного ключа (A B -> C D, B -> C)
        ((S("a b c d"), F("a b -> d; b -> c")), "1NF"),
        # Тест 2: Схема 3NF, але не BCNF (student subject -> teacher, teacher -> subject)
        ((S("student subject teacher"), F("student subject -> teacher; teacher -> subject")), "3NF"),
        # Тест 3: Чиста схема BCNF (a -> b, b -> c, c -> d з єдиним ключем a)
        ((S("a b"), F("a -> b")), "BCNF"),
    ],
)
def test_my_cases(args, expected):
    check(M.normal_form, args, expected)