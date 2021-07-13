
from functools import reduce, partial
from itertools import tee, islice, chain


from streams.Transducer import Transducer
from streams.generator_utilities import empty_iterator
from streams.utilities import default_reduce_initializer, executewith, executeasync


class Stream(Transducer):
    def __init__(self, partials=[], data=None):
        self.partials=partials
        self.__catch_all_fn = None
        self.data = data

    def length(self):
        def partiallengthfunction(data):
            return len(list(data))

        self.add_partial(partiallengthfunction)
        return self.execute()

    def reduce(self, fn,initial_value=default_reduce_initializer):
        super(Stream, self).reduce(fn,initial_value)
        return self

    def asList(self):
        response = self.execute()
        return list(response)

    def asSet(self):
        response = self.execute()
        return set(response)

    def asSingle(self):
        response = self.execute()
        return next(response)



    def stream(self):
        self.data, other = tee(self.data)
        return Stream(self.partials.copy(), other)

    def pipe(self, transducer):
        self.partials = list(chain(transducer.partials, self.partials))
        return self

    def catchAll(self, fn):
        self.__catch_all_fn = fn
        return self



    def execute(self):
        result = self.data
        #
        # for currentpartial in self.partials:
        #     result = currentpartial(result)
        # return result
        #result= self.data



        for partialfn in self.partials:
            try:
                result = partialfn(result)
            except Exception as inst:
                self.handleException(inst,partialfn,result)
                return empty_iterator()

        return result
        #result= self.data


        #return reduce(lambda acc,partialfn:executepartial(acc,partialfn),self.partials,self.data)

    def handleException(self, inst,partialfn,currentdata):
        error_data = {"error": str(type(inst)) + "Error while Executing Function ", "function-data": partialfn,
                      "args": inst.args,"currentdata":currentdata, "exception": inst}
        if self.__catch_all_fn is not None:
            self.__catch_all_fn(error_data)
        else:
            raise Exception(error_data)

    @staticmethod
    def create(data):
        return Stream([], data=data)

    @staticmethod
    def transducer():
        return Transducer([])

    @staticmethod
    def compose():
        return Transducer([])
