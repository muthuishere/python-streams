from functools import reduce
from itertools import tee

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
        self.data = filter(fn, self.data)
        return self

    def peek(self, fn):
        def peekfunction(val):
            fn(val)
            return val

        self.data = map(peekfunction, self.data)
        return self

    def skip(self, number):
        for i in range(number):
            next(self.data)

        return self

    def take(self, number):
        results = self.__convert_as_list()
        updated_value = results[:number]
        self.data = generator_from_list(updated_value)
        return self

    def distinct(self):
        results = self.__convert_as_list()
        unique_items = list(set(results))
        self.data = generator_from_list(unique_items)
        return self

    def flatmap(self, fn):
        data = map(fn, self.data)
        self.data = generator_from_list_of_lists(data)
        return self

    def __create_a_copy(self):
        self.data, other = tee(self.data)
        return other

    def __convert_as_list(self):
        return list(self.data)

    def stream(self):
        result = self.__create_a_copy()
        return Stream(result)

    def length(self):
        results = self.__convert_as_list()
        return len(results)

    def asList(self):
        result = self.__convert_as_list()
        return result

    def reduce(self, fn):
        return reduce(fn, self.data)

    @staticmethod
    def create(data):
        return Stream(generator_from_list(data))
