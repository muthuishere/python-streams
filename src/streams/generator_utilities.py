
def create_generator_with_first_value_twice(data):
    first = next(data)
    yield from send_same_number_n_times(first,2)
    for i in data:
        yield i


def send_same_number_n_times(first, stop=1):
    for i in range(stop):
        yield first



def split_first_value_data_type_and_generator(data):
    data_generator = create_generator_with_first_value_twice(data)
    first_value = next(data_generator)
    data_type = type(first_value)
    return first_value, data_type, data_generator

#
# isinstance("10", str)
# isinstance(10, int)
# isinstance({"name":"Mrx"}, dict)
# isinstance(["name","Mrx"], list)

def split_first_value_and_generator(data):
    (first_value, data_type, data_generator) = split_first_value_data_type_and_generator(data)
    return first_value, data_generator

def empty_iterator():
    yield