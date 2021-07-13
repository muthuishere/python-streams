import csv
import os

from streams.Stream import Stream
from streams.data_checker import isDict
from streams.generator_utilities import split_first_value_and_generator
from streams.utilities import generator_from_file, generator_from_csv


class FileStream(Stream):
    def __init__(self,data):
        super(FileStream, self).__init__(partials = [], data = data)

    def asFileWithContents(self, filename, data, lineseperator):
        results = data
        contents = lineseperator.join((str(item)).rstrip() for item in results)
        with open(filename, "w") as f:
            f.write(contents)

        return True

    def asTextFile(self, filename, lineseperator="\n"):
        response = self.execute()
        return self.asFileWithContents(filename,response,lineseperator)

    def asCSV(self,filename,delimiter=',', lineseperator="\n"):

        def write_as_csv(data):
            first_value,results =split_first_value_and_generator(data)
            if isDict(first_value) == False:
                return self.asFileWithContents(filename,results,lineseperator)

            fieldnames = first_value.keys()
            with open(filename, "w", encoding="utf-8", newline=lineseperator) as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows((item for item in results))
            return True


        response = self.execute()
        return write_as_csv(response)






    @staticmethod
    def createFromText(filename):
        data = generator_from_file(filename)
        return FileStream(data=data)


    @staticmethod
    def createFromCsv(filename,encoding ='utf-8-sig' ):
        data = generator_from_csv(filename,encoding)
        return FileStream(data=data)


