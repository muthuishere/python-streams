from functools import reduce, partial
from itertools import tee, islice

from streams.utilities import generator_from_list_of_lists, generator_from_list


class Stream():
    def __init__(self,partials = [],data = None):
        self.partials = partials
        self.data = data

    def map(self, fn):
        partial_function= partial(map,fn)
        self.partials.append(partial_function)
        return self

    def filter(self, fn):
        partial_function = partial(filter, fn)
        self.partials.append(partial_function)
        return self

    def peek(self, fn):
        def peekfunction(fn,val):
            fn(val)
            return val

        def partialpeekfunction(data,fn):
            return map(lambda val:peekfunction(fn,val), data)

        partial_function = partial(partialpeekfunction, fn=fn)
        self.partials.append(partial_function)
        return self

    def skip(self, number):
        def skipfunction(data,number):
            return islice(data,number,None)

        partial_function = partial(skipfunction, number=number)
        self.partials.append(partial_function)
        return self

    def take(self, number):
        def takefunction(data,number):
            return islice(data, number)

        partial_function = partial(takefunction, number=number)
        self.partials.append(partial_function)
        return self

    def distinct(self):
        def distinctfunction(data):
            results = list(data)
            unique_items = list(set(results))
            return generator_from_list(unique_items)

        self.partials.append(distinctfunction)
        return self

    def flatmap(self, fn):
        def flatmapfunction(fn,input):
            data = map(fn, input)
            return generator_from_list_of_lists(data)

        partial_flatmap_function = partial(flatmapfunction, fn)
        self.partials.append(partial_flatmap_function)
        return self



    def length(self):
        def lengthfunction(data):
            return len(list(data))

        self.partials.append(lengthfunction)
        return self.execute(self.data)

    def asList(self):
        def asListFunction(data):
            return list(data)

        self.partials.append(asListFunction)
        return self.execute(self.data)

    def reduce(self, fn):
        partial_function = partial(reduce, fn)
        self.partials.append(partial_function)

        return self.execute(self.data)

    def stream(self):
        self.data, other = tee(self.data)
        return Stream(self.partials.copy(),other)

    def execute(self,data):
        result=data
        for partial in self.partials:
            result = partial(result)
        return result

    @staticmethod
    def create(data):
        return Stream([],data=data)


