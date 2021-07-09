from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.profiler import start_profiler, stop_profiler
from shared.users import get_users

import cProfile
import pstats

from streams.Stream import Stream
from users import get_200_users


class TestStreamOthers(BaseUnitTest):
    def test_compose_functions_functional_stream_long_method(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()

        start_profiler()

        #531 function calls in 0.001 seconds
        product_stream = Stream.create(products)
        total_products_with_rating_greater_than_3 = (product_stream
                          .stream()
                          .filter(is_rating_greater_than_three)
                          .length())
        prices_for_clothes = (product_stream
                                .stream()
                                .filter(is_clothing)
                                .map(price_from_product)
                                .distinct()
                                .skip(5)
                                .take(8)
                                .asList()
                                )

        stop_profiler()
        print(total_products_with_rating_greater_than_3)
        print(prices_for_clothes)
        self.assertEqual(57,total_products_with_rating_greater_than_3)
        self.assertListEqualsInAnyOrder([2795.0, 2699.0, 750.0, 1199.0, 2299.0, 1200.0, 1299.0, 1499.0],prices_for_clothes)

    def test_compose_functions_users_functional_stream(self):
        #200 Records
        #710 function calls in 0.001 seconds
        is_salary_greater_than_5000 = lambda user: user['salary'] > 50000
        is_male = lambda user: user['gender'] == "Male"
        name_from_user = lambda user: user['first_name']
        users = get_200_users()


        start_profiler()
        #Previous 710 function calls in 0.001 seconds
        #706 function calls in 0.001 seconds
        results = (Stream.create(users)
                     .filter(is_salary_greater_than_5000)
                     .filter(is_male)
                     .map(name_from_user)
                     .asList()
                     )

        stop_profiler()

        print("results", results)
        self.assertListContains(
            ['Jasen', 'Vasili', 'Lind', 'Darbee', 'Britte', 'Layton', 'Rosabelle', 'Wiley', 'Timoteo', 'Cly', 'Syman',
             'Windham'], results)