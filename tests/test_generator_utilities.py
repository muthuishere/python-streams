from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from streams.data_checker import isInt
from streams.Stream import Stream
from streams.generator_utilities import empty_iterator, split_first_value_and_generator
from streams.utilities import generator_from_list


class Test(BaseUnitTest):
    def test_split_data_type_and_generator(self):
        first_value,generator_values = split_first_value_and_generator(generator_from_list(range(10)))
        self.assertTrue(isInt(first_value))
        self.assertListEqualsInAnyOrder(range(10),list(generator_values))

    def test_empty_iterator_yields_one_none_so_caught_errors_are_not_empty(self):
        self.assertEqual([None], list(empty_iterator()))
        self.assertEqual((None,), tuple(empty_iterator()))

        def failing_reduce(accumulator, value):
            raise ValueError('reduce failed')

        def catch_all_exception(error_data):
            return None

        caught_as_list = (Stream
                          .create([1, 2])
                          .reduce(failing_reduce)
                          .catchAll(catch_all_exception))
        self.assertEqual([None], caught_as_list.asList())

        caught_as_single = (Stream
                            .create([1, 2])
                            .reduce(failing_reduce)
                            .catchAll(catch_all_exception))
        self.assertIsNone(caught_as_single.asSingle())
