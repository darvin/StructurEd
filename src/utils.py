
def get_or_create_dict_element(dictionary, key, default_value):
    if key in dictionary:
        return dictionary[key]
    else:
        dictionary[key] = default_value
        return dictionary[key]