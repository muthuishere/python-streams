import multiprocessing
from functools import reduce, partial
from itertools import tee, islice, chain
from multiprocessing.pool import ThreadPool as Pool

from streams.utilities import generator_from_list_of_lists, generator_from_list, default_reduce_initializer


class Transducer():
    def __init__(self, partials=[]):
        self.partials = partials

    def add_partial(self, partialfn):
            self.partials.append(partialfn)

        
    def add_partial_to_transducer(self, partialfn):
            self.add_partial(partialfn)


    def map(self, fn):
        self.add_partial_to_transducer(partial(map, fn))
        return self

    def filter(self, fn):
        self.add_partial_to_transducer(partial(filter, fn))
        return self

    def distinct(self):
        def partialdistinctfunction(data):
            unique_items = set(data)
            return generator_from_list(unique_items)

        self.add_partial_to_transducer(partialdistinctfunction)
        return self

    def reduce(self, fn,initial_value=default_reduce_initializer):
        def partialReduceFunction(data,fn,initial_value):
            result = []
            result.append(reduce(fn,data,initial_value))
            return generator_from_list(result)

        self.add_partial_to_transducer(partial(partialReduceFunction,initial_value=initial_value,fn=fn))

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

    def peek(self, fn):
        def peekfunction(fn, val):
            fn(val)
            return val

        def partialpeekfunction(data, fn):
            return map(lambda val: peekfunction(fn, val), data)

        self.add_partial_to_transducer(partial(partialpeekfunction, fn=fn))
        return self

    def skip(self, number):
        def partialskipfunction(data, number):
            return islice(data, number, None)
        self.add_partial_to_transducer(partial(partialskipfunction, number=number))
        return self

    def take(self, number):
        def partialtakefunction(data, number):
            return islice(data, number)


        self.add_partial_to_transducer(partial(partialtakefunction, number=number))
        return self



    def flatmap(self, fn):
        def partialflatmapfunction(fn, input):
            data = map(fn, input)
            return generator_from_list_of_lists(data)

        self.add_partial_to_transducer(partial(partialflatmapfunction, fn))
        return self

    @staticmethod
    def create(partials = []):
        return Transducer(partials)


