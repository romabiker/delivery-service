

def float_or_none(value) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        ...
