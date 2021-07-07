from functools import reduce


def generator_from_list(data):
    for row in data:
        yield row

def generator_from_list_of_lists(toplist):
    for values in toplist:
        for value in values:
            yield value


class Stream():
    def __init__(self, data):
        self.data = data

    def map(self, fn):
        return Stream(map(fn, self.data))


    def peek(self, fn):
        results = self.__get_as_value()
        for result in results:
            fn(result)
        return Stream(generator_from_list(results))


    # Validate Skip is not doing any issues for generator object
    def skip(self, number):
        results = self.__get_as_value()
        updated_value = results[number:]
        return Stream(generator_from_list(updated_value))

    def take(self, number):
        results = self.__get_as_value()
        updated_value = results[:number]
        return Stream(generator_from_list(updated_value))

    def distinct(self):
        results = self.__get_as_value()
        unique_items = list(set(results))
        return Stream(generator_from_list(unique_items))

    def length(self):
        results = self.__get_as_value()
        return len(results)

    def flatmap(self, fn):
        results = self.__get_as_value()
        result = map(fn, results)
        return Stream(generator_from_list_of_lists(result))

    def filter(self, fn):
        return Stream(filter(fn, self.data))


    # To Avoid Generator Corruption, Copy it
    def __get_as_value(self):
        result = list(self.data)
        self.data = generator_from_list(result)
        return result

    def reduce(self, fn):
        result = self.__get_as_value()
        return reduce(fn, result)

    def stream(self):
        result = self.__get_as_value()
        return Stream(generator_from_list(result))

    def asList(self):
        result = self.__get_as_value()
        return result

    @staticmethod
    def create(data):
        return Stream(generator_from_list(data))



