import operator
from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.profiler import start_profiler, stop_profiler
from shared.users import get_users

import cProfile
import pstats

from streams.Stream import Stream


class TestFilterComposeStream(BaseUnitTest):

    def test_compose_functions_functional_stream(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()

        # 976 function calls in 0.001 seconds functional-streams
        product_stream = Stream.create(products)
        total_products = (product_stream
                          .stream()
                          .filter(is_rating_greater_than_three)
                          .length())
        reviews_for_clothing = (product_stream
                                .stream()
                                .filter(is_clothing)
                                .map(price_from_product)
                                .asList()
                                )

        stop_profiler()
        print(total_products)
        print(reviews_for_clothing)

    def test_create(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()

        product_stream = Stream.create(products)

        reviews_for_clothing = (product_stream
                                .stream()
                                .filter(is_clothing)
                                .peek(lambda val: print("is_clothing", val))
                                .map(price_from_product)
                                .asList()
                                )

        total_products = (product_stream
                          .stream()
                          .filter(is_rating_greater_than_three)
                          .length())

        stop_profiler()
        print(total_products)
        print(reviews_for_clothing)
        self.assertEqual(57, total_products)
        self.assertListContains(
            [999.0, 699.0, 1199.0, 1199.0, 2299.0, 999.0, 999.0, 2499.0, 2400.0, 1299.0, 699.0, 2199.0, 999.0, 1200.0,
             899.0, 899.0, 1399.0, 1499.0, 750.0, 1299.0, 5398.0, 2795.0, 4999.0, 2699.0, 2499.0], reviews_for_clothing)
