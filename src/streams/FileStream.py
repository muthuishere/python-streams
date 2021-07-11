import csv
import io
from functools import reduce, partial
from itertools import tee, islice, chain

from streams.Stream import Stream
from streams.Transducer import Transducer
from streams.utilities import default_reduce_initializer, executewith, executeasync, generator_from_file


class FileStream(Stream):
    def __init__(self,data):
        super(FileStream, self).__init__(partials = [], data = data)



    def asFile(self,filename):
        def partialAsFileFunction(data):
            with open(filename, "w") as f:
                f.write("".join(str(item) for item in data))

            return True


        response = self.execute()
        return partialAsFileFunction(response)







    @staticmethod
    def create(filename):
        data = generator_from_file(filename)
        return FileStream(data=data)


