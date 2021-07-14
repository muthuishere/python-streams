class DictItem(object):

    def __init__(self, key):
        if key == None:
            self.valueFunction = lambda inp: inp;
        else:
            self.valueFunction = lambda inp: inp[key];

    def __getitem__(self, key):
        return DictItem(key)

    def __call__(self, inp):
        return self.valueFunction(inp)  # inp[self.key]

    def print(self, inp):
        print(inp)

    def sum(self, a, b):
        return a + self.valueFunction(b)

    def isodd(self, input):
        return (self.valueFunction(input) % 2) != 0

    def iseven(self,input):
        return (self.valueFunction(input) % 2) != 0

    def startswith(self, comparableValue):
        return lambda inp: self.valueFunction(inp).startswith(comparableValue)

    def __eq__(self, other):
        return lambda inp: self.valueFunction(inp) == other

    def __add__(self, other):
        return lambda inp: self.valueFunction(inp) + other

    def __truediv__(self, other):
        return lambda inp: self.valueFunction(inp) / other

    def __floordiv__(self, other):
        return lambda inp: self.valueFunction(inp) // other

    def __pow__(self, other):
        return lambda inp: self.valueFunction(inp) ** other

    def __rshift__(self, other):
        return lambda inp: self.valueFunction(inp) >> other

    def __lshift__(self, other):
        return lambda inp: self.valueFunction(inp) << other

    def __and__(self, other):
        return lambda inp: self.valueFunction(inp) & other

    def __or__(self, other):
        return lambda inp: self.valueFunction(inp) | other

    def __xor__(self, other):
        return lambda inp: self.valueFunction(inp) ^ other

    def __mod__(self, other):
        return lambda inp: self.valueFunction(inp) % other

    def __mul__(self, other):
        return lambda inp: self.valueFunction(inp) * other

    def __sub__(self, other):
        return lambda inp: self.valueFunction(inp) - other

    def __gt__(self, other):
        return lambda inp: self.valueFunction(inp) > other

    def __lt__(self, other):
        return lambda inp: self.valueFunction(inp) < other


item = DictItem(None)
