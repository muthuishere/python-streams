import operator
from unittest import TestCase

from shared.products import get_products
from shared.users import get_users
from streams.Stream import Stream
from streams.operations.operators import item


class TestOperators(TestCase):

    def test_value_map_numbers(self):
        results = (Stream
                   .create(range(5))
                   .reduce(operator.add)
                   .asSingle())
        self.assertEqual(results, 10)


def test_value_map(self):
    results = (Stream
               .create(get_users())
               .map(item['gender'])
               .asList())
    self.assertEqual(results,
                     ['Female', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Male',
                      'Female', 'Male', 'Agender', 'Polygender', 'Male', 'Male', 'Polygender', 'Female', 'Male',
                      'Male', 'Non-binary', 'Polygender', 'Male', 'Non-binary', 'Male'])


def test_filter(self):
    results = (Stream
               .create(get_users())
               .filter(item['gender'] == 'Male')
               .map(item['gender'])
               .asList())
    self.assertEqual(len(results), 12)


def test_filter_compose_get_products(self):
    results = (Stream
               .create(get_products())
               .filter(item['category'] == 'Clothing')
               .flatmap(item['reviews'])
               .peek(item.print)
               .map(item['user'])
               .asList())
    print(results)
    self.assertEqual(len(results), 39)


def test_reduce_operator(self):
    sum_of_salaries = (Stream
                       .create(get_users())
                       .filter(item['gender'] == 'Male')
                       .reduce(item['salary'].sum)
                       .asSingle()
                       )
    self.assertEqual(sum_of_salaries, 977023)


def test_map_check(self):
    users = get_users()
    result = item['gender'](users[0])
    self.assertEqual(result, 'Female')


def test_filter_check(self):
    users = get_users()
    first_user = users[0]
    curValue = item['gender']
    result = (curValue == 'Female')
    finalResult = result(first_user)
    self.assertEqual(finalResult, True)


def test_map_filter_check(self):
    users = get_users()
    first_user = users[0]

    curValue = item['gender']
    result = (curValue == 'Female')
    finalResult = result(first_user)
    self.assertEqual(finalResult, True)
    result = curValue(users[0])
    self.assertEqual(result, 'Female')
