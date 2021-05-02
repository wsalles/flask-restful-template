def non_empty_value(_value):
    if not _value:
        raise ValueError("Must not be an empty value")
    return _value
