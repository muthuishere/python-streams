from functools import reduce, partial
from itertools import tee, islice, chain

from streams.utilities import generator_from_list_of_lists, generator_from_list


class Stream():
    def __init__(self, partials=[], data=None):
        self.partials = partials
        self.data = data

    def map(self, fn):
        self.partials.append(partial(map, fn))
        return self

    def filter(self, fn):
        self.partials.append(partial(filter, fn))
        return self

    def peek(self, fn):
        def peekfunction(fn, val):
            fn(val)
            return val

        def partialpeekfunction(data, fn):
            return map(lambda val: peekfunction(fn, val), data)

        self.partials.append(partial(partialpeekfunction, fn=fn))
        return self

    def skip(self, number):
        def partialskipfunction(data, number):
            return islice(data, number, None)

        self.partials.append(partial(partialskipfunction, number=number))
        return self

    def take(self, number):
        def partialtakefunction(data, number):
            return islice(data, number)

        self.partials.append(partial(partialtakefunction, number=number))
        return self

    def distinct(self):
        def partialdistinctfunction(data):
            results = list(data)
            unique_items = list(set(results))
            return generator_from_list(unique_items)

        self.partials.append(partialdistinctfunction)
        return self

    def flatmap(self, fn):
        def partialflatmapfunction(fn, input):
            data = map(fn, input)
            return generator_from_list_of_lists(data)

        self.partials.append(partial(partialflatmapfunction, fn))
        return self

    def length(self):
        def partiallengthfunction(data):
            return len(list(data))

        self.partials.append(partiallengthfunction)
        return self.execute(self.data)

    def asList(self):
        def partialAsListFunction(data):
            return list(data)

        self.partials.append(partialAsListFunction)
        return self.execute(self.data)

    def reduce(self, fn):
        self.partials.append(partial(reduce, fn))
        return self.execute(self.data)

    def stream(self):
        self.data, other = tee(self.data)
        return Stream(self.partials.copy(), other)

    def pipe(self, transducer):
        self.partials = list(chain(transducer.partials, self.partials))
        return self

    def execute(self, data):
        result = data
        for partial in self.partials:
            result = partial(result)
        return result

    @staticmethod
    def create(data):
        return Stream([], data=data)

    @staticmethod
    def transducer():
        return Stream([], data=None)
