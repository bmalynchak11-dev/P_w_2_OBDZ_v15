from helpers import S, F

ATTRS = S("tx_id tx_date amount user_id user_email category_id category_name")

FDS = F(
    "tx_id -> tx_date amount user_id category_id; "
    "user_id -> user_email; "
    "category_id -> category_name"
)

KEYS = {S("tx_id")}

NORMAL_FORM = "2NF"

PARTS = [
    S("tx_id tx_date amount user_id category_id"),
    S("user_id user_email"),
    S("category_id category_name"),
]