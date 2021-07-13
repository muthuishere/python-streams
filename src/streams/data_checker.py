# isinstance("10", str)
# isinstance(10, int)
# isinstance({"name":"Mrx"}, dict)
# isinstance(["name","Mrx"], list)


def isList(data):
    return isinstance(data, list)

def isDict(data):
    return isinstance(data, dict)

def isString(data):
    return isinstance(data, str)

def isInt(data):
    return isinstance(data, int)