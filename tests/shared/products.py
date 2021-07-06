import json
import os
from pathlib import Path

#Path(__file__).parent.absolute()
# f = open(get_current_path() + '\\products.json')
# products = json.load(f)
# f.close()
# return products

def get_current_path():
    return str(Path(__file__).parent.absolute())

def get_products():

    f = open(get_current_path() + '\\products.json')
    products = json.load(f)
    f.close()
    return products


if __name__ == '__main__':
    print(get_products())