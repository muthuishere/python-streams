from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from streams.data_checker import isInt
from streams.generator_utilities import split_first_value_and_generator
from streams.utilities import generator_from_list


class Test(BaseUnitTest):
    def test_split_data_type_and_generator(self):
        first_value,generator_values = split_first_value_and_generator(generator_from_list(range(10)))
        self.assertTrue(isInt(first_value))
        self.assertListEqualsInAnyOrder(range(10),list(generator_values))
