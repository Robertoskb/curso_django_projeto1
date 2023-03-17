def is_possitive(value):
    try:
        number = float(value)

    except ValueError:
        return False

    return number > 0
