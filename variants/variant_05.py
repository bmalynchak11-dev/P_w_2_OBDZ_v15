"""
Задача 5. Нормальна форма схеми (Варіант 15, Набір 3)
"""
from itertools import combinations


def _compute_closure(x, fds):
    """Обчислення замикання X+ відносно списку залежностей fds."""
    res = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(res):
                diff = rhs - res
                if diff:
                    res.update(diff)
                    changed = True
    return frozenset(res)


def _find_candidate_keys(attrs, fds):
    """Знаходження всіх ключів-кандидатів схеми."""
    attrs_set = frozenset(attrs)
    keys = []
    
    # Визначаємо атрибути, яких немає в правих частинах FDs (вони обов'язково є в кожному ключі)
    rhs_all = set()
    for _, rhs in fds:
        rhs_all.update(rhs)
    core = attrs_set - rhs_all
    
    if _compute_closure(core, fds) == attrs_set:
        return [core]
        
    remaining = list(attrs_set - core)
    
    for r in range(1, len(remaining) + 1):
        for combo in combinations(remaining, r):
            candidate = core.union(combo)
            # Перевірка на мінімальність: кандидат не повинен містити вже знайдений ключ
            if any(k.issubset(candidate) for k in keys):
                continue
            if _compute_closure(candidate, fds) == attrs_set:
                keys.append(candidate)
                
    return keys if keys else [attrs_set]


def normal_form(attrs, fds):
    """
    Визначає найвищу нормальну форму схеми: '1NF', '2NF', '3NF' або 'BCNF'.
    Вхідні структури не мутуються.
    """
    attrs_set = frozenset(attrs)
    
    # Фільтруємо залежності, прибираючи тривіальні (де rhs є підмножиною lhs)
    non_trivial_fds = [(frozenset(lhs), frozenset(rhs - lhs)) for lhs, rhs in fds if (rhs - lhs)]
    
    # Якщо нетривіальних залежностей немає взагалі — схема автоматично в BCNF
    if not non_trivial_fds:
        return "BCNF"
        
    candidate_keys = _find_candidate_keys(attrs_set, non_trivial_fds)
    
    # Первинні атрибути (входять хоча б в один ключ-кандидат)
    prime_attrs = set()
    for k in candidate_keys:
        prime_attrs.update(k)
        
    # Функція перевірки, чи є підмножина надключем
    def is_superkey(x):
        return _compute_closure(x, non_trivial_fds) == attrs_set

    # 1. Перевірка на 2NF:
    # Жоден неключовий атрибут не повинен залежати від власної підмножини ключа-кандидата.
    for k in candidate_keys:
        if len(k) > 1:
            for r in range(1, len(k)):
                for proper_subset in combinations(k, r):
                    sub_closure = _compute_closure(frozenset(proper_subset), non_trivial_fds)
                    for non_prime in sub_closure - frozenset(proper_subset):
                        if non_prime not in prime_attrs and non_prime in attrs_set:
                            return "1NF"

    # 2. Перевірка на 3NF:
    # Для кожної X -> A (де A — один атрибут, A not in X): X має бути надключем АБО A є первинним.
    for lhs, rhs in non_trivial_fds:
        if not is_superkey(lhs):
            for attr in rhs:
                if attr not in prime_attrs:
                    return "2NF"

    # 3. Перевірка на BCNF:
    # Для кожної нетривіальної залежності X -> Y: X обов'язково є надключем.
    for lhs, rhs in non_trivial_fds:
        if not is_superkey(lhs):
            return "3NF"

    return "BCNF"