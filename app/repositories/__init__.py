from typing import Dict


def generate_query_filter(filters: Dict) -> str:
    if not filters:
        return

    query = "WHERE "
    parameters = ""

    it = iter(filters)
    f = next(it, None)

    while f:
        parameters += f"{f} = ? "
        f = next(it, None)
        if f:
            parameters += f"AND "

    return query + parameters
