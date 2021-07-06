from functools import reduce


def generator_from_list(data):
    for row in data:
        yield row


class Stream():
    def __init__(self, data):
        self.data = data

    def map(self, fn):
        self.data = map(fn, self.data)
        return self

    def peek(self, fn):
        results = self.__get_as_value()
        for result in results:
            fn(result)
        return self

    # Validate Skip is not doing any issues for generator object
    def skip(self, number):
        for n in range(number):
            next(self.data)
        return self

    def take(self, number):
        items = []
        for n in range(number):
            items.append(next(self.data))
        self.data = generator_from_list(items)
        return self

    def distinct(self):
        results = self.__get_as_value()
        unique_items = list(set(results))
        self.data = generator_from_list(unique_items)
        return self

    def length(self):
        results = self.__get_as_value()
        return len(results)

    def flatmap(self, fn):
        result = map(fn, self.data)
        return Stream(generator_from_list(next(result)))

    def filter(self, fn):
        self.data = filter(fn, self.data)
        return self

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



