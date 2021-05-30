import csv

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

def open_read_csv_file(file_to_read_in):
    file_obj = open(file_to_read_in, 'r', newline='')
    csv_object = csv.reader(file_obj)
    next(csv_object)
    return csv_object

def create_dictionary_object(csv_object) -> dict:
    dictionary_object = {}
    for row in csv_object:
        key = row[0]
        row = row[1:]
        for data in row:
            if not data == '':
                append_value(dictionary_object, key, data)
    return dictionary_object
