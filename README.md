# Стартовий проєкт OBDZ-P02

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні, PostgreSQL не потрібен.
4. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py` і свою схему `my_schema/schema.py`.
5. Описи таблиць для власного аналізу лежать у `data/own_domain_N.md`, приклади даних у `data/own_domain_N.csv`. Перевірка власної схеми: `python check_my_schema.py N`. Частина Б (таблиця з вашого дипломного проєкту): опис у `my_schema/diploma_table.md`, дані в `my_schema/diploma_table.csv`, схема в `my_schema/diploma_schema.py`, перевірка: `python check_my_schema.py own my_schema/diploma_schema.py my_schema/diploma_table.csv`.
