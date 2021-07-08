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
        self.data = map(fn, self.data)
        return self

    def filter(self, fn):
        return Stream(filter(fn, self.data))

    def peek(self, fn):
        def peekfunction(val):
            fn(val)
            return val

        self.data = map(peekfunction, self.data)
        return self

    # Validate Skip is not doing any issues for generator object
    def skip(self, number):
        results = self.__convert_as_list()
        updated_value = results[number:]
        return Stream(generator_from_list(updated_value))

    def take(self, number):
        results = self.__convert_as_list()
        updated_value = results[:number]
        return Stream(generator_from_list(updated_value))

    def distinct(self):
        results = self.__convert_as_list()
        unique_items = list(set(results))
        return Stream(generator_from_list(unique_items))

    def length(self):
        results = self.__convert_as_list()
        return len(results)

    def flatmap(self, fn):
        result = map(fn, self.data)
        return Stream(generator_from_list_of_lists(result))



    def __create_a_copy(self):
        result = list(self.data)
        self.data = generator_from_list(result)
        return result

    def __convert_as_list(self):
        return list(self.data)

    def reduce(self, fn):
        return reduce(fn, self.data)

    def stream(self):
        result = self.__create_a_copy()
        return Stream(generator_from_list(result))

    def asList(self):
        result = self.__convert_as_list()
        return result

    @staticmethod
    def create(data):
        return Stream(generator_from_list(data))
