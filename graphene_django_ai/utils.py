def tuple_keys_contain_str(tuple_data):
    has_str = False
    for item in tuple_data:
        if not isinstance(item[0], int):
            has_str = True
            break

    return has_str
