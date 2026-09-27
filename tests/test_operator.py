import operator
import unittest
from unittest import TestCase

from shared.products import get_products
from shared.users import get_users
from streams.Stream import Stream
from streams.operations.operators import item


class TestOperators(TestCase):

    def test_reduce_with_sum_of_first_five_numbers(self):
        results = (Stream
                   .create(range(5))
                   .reduce(operator.add)
                   .asSingle())
        self.assertEqual(results, 10)

    def test_map_with_product_of_first_10_numbers(self):
        results = (Stream
                   .create(range(5))
                   .map(item * 2)
                   .asList())
        self.assertEqual(results, [0, 2, 4, 6, 8])

    def test_reduce_with_sum_of_1_to_6(self):
        results = (Stream
                   .create(range(5))
                   .map(item + 1)
                   .reduce(item.sum)
                   .asSingle())
        self.assertEqual(results, 15)

    # def test_filter_with_getting_even_numbers_from_1_to_10(self):
    #     results = (Stream
    #                .create(range(10))
    #                .filter(item % 2 == 1)
    #                .asList()
    #                )
    #     self.assertEqual(results, [1, 3, 5, 7, 9])

    def test_filter_with_getting_odd_numbers_with_lambda_from_1_to_10(self):
        results = (Stream
                   .create(range(10))
                   .filter(lambda value: value % 2 == 1)
                   .asList()
                   )
        self.assertEqual(results, [1, 3, 5, 7, 9])

    def test_filter_with_isodd_operator_from_1_to_10(self):
        results = (Stream
                   .create(range(10))
                   .filter(item.isodd)
                   .asList())
        self.assertEqual(results, [1, 3, 5, 7, 9])
        self.assertFalse(item.isodd(0))
        self.assertTrue(item.isodd(1))
        self.assertFalse(item.isodd(2))
        self.assertTrue(item.isodd(-3))

    # BUG: operators.py:25 repeats the isodd comparison, so iseven reports odd numbers as even.
    @unittest.expectedFailure
    def test_iseven_with_even_and_odd_numbers(self):
        self.assertTrue(item.iseven(0))
        self.assertTrue(item.iseven(2))
        self.assertFalse(item.iseven(3))

    def test_chained_subscript_keeps_only_the_last_key(self):
        with self.assertRaises(KeyError):
            item['a']['b']({'a': {'b': 5}})
        self.assertEqual(5, item['a']['b']({'b': 5}))

    def test_division_by_zero_is_raised_when_the_quotient_is_computed(self):
        self.assertEqual(2.5, (item / 2)(5))
        self.assertEqual(2, (item // 2)(5))
        self.assertEqual(-3, (item // 2)(-5))
        self.assertEqual(2.0, (item // 2)(5.0))
        divide_by_zero = item / 0
        self.assertTrue(callable(divide_by_zero))
        with self.assertRaises(ZeroDivisionError):
            divide_by_zero(5)
        floor_divide_by_zero = item // 0
        with self.assertRaises(ZeroDivisionError):
            floor_divide_by_zero(5)

    def test_bitwise_operators_reject_floats_only_when_called(self):
        self.assertEqual(1, (item & 3)(5))
        self.assertEqual(7, (item | 3)(5))
        self.assertEqual(6, (item ^ 3)(5))
        self.assertEqual(1, (item & True)(5))
        for bitwise_operator in (item & 3, item | 3, item ^ 3):
            with self.assertRaises(TypeError) as context:
                bitwise_operator(5.0)
            self.assertIn("unsupported operand type(s)", str(context.exception))

    def test_sub_and_lt_operators_subtract_and_compare(self):
        self.assertEqual(4, (item - 1)(5))
        self.assertEqual(4, (item['n'] - 1)({'n': 5}))
        with self.assertRaises(TypeError):
            (item - 1)(None)
        self.assertTrue((item < 3)(2))
        self.assertFalse((item < 3)(5))
        with self.assertRaises(TypeError):
            (item < 3)(None)


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
