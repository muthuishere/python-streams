

def generator_from_list(data):
    for row in data:
        yield row


def generator_from_list_of_lists(toplist):
    for values in toplist:
        for value in values:
            yield value