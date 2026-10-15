"""
Власна схема для data/own_domain_3.csv
Стовпці: group_code, curator, subject, teacher, hours
"""
import sys
from pathlib import Path

# Додаємо теку tests для імпорту helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tests"))

from helpers import S, F

# 1. Атрибути таблиці
ATTRS = S("curator group_code hours subject teacher")

# 2. Функціональні залежності чітко за правилами предметної області:
# - у кожної групи є один куратор: group_code -> curator
# - для пари «група, дисципліна» задано викладача й кількість годин: group_code subject -> hours teacher
# - кожен викладач веде лише одну дисципліну: teacher -> subject
FDS = F(
    "group_code -> curator; "
    "group_code subject -> hours teacher; "
    "teacher -> subject"
)

# 3. Ключі-кандидати таблиці:
# Оскільки teacher -> subject, то (group_code, teacher) також визначає subject,
# а отже й hours. Тобто ключів два:
KEYS = {S("group_code subject"), S("group_code teacher")}

# 4. Нормальна форма: 1NF
# curator залежить від частини ключа group_code (group_code -> curator),
# що є частковою залежністю, тому 2NF порушено.
NORMAL_FORM = "1NF"

# 5. Декомпозиція без втрат у 3NF зі збереженням залежностей:
# R1(group_code, curator) зберігає group_code -> curator
# R2(teacher, subject) зберігає teacher -> subject
# R3(group_code, teacher, hours) зберігає навантаження групи з викладачем (або group_code, subject, hours)
PARTS = [
    S("group_code curator"),
    S("subject teacher"),
    S("group_code teacher hours"),
]