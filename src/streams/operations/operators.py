

class DictItem(object):

    def __init__(self, key):
        self.key = key

    def __getitem__(self, key):
            return DictItem(key)

    def __call__(self, inp):
        return inp[self.key]

    def print(self, inp):
        print(inp)

    def sum(self, a, b):
        return a + b[self.key]



    def startswith(self, comparableValue):
        key = self.key
        return lambda inp: inp[key].startswith(comparableValue)

    def __eq__(self, comparableValue):
        key = self.key
        return lambda inp: inp[key] == comparableValue

    def __gt__(self, comparableValue):
        key = self.key
        return lambda inp: inp[key] > comparableValue

    def __lt__(self, comparableValue):
        key = self.key
        return lambda inp: inp[key] < comparableValue


item = DictItem(None)
