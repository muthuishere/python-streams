import operator
from unittest import TestCase

from shared.products import get_products
from shared.users import get_users

import cProfile
import pstats

from streams.Stream import Stream


class TestStream(TestCase):
    def test_create(self):
        results = Stream.create(get_users()).asList()
        self.assertEqual(25, len(results))

    def test_map(self):
        results = (Stream
                   .create(get_users())
                   .map(lambda user: user['gender'])
                   .asList())
        self.assertEqual(results,
                         ['Female', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Male',
                          'Female', 'Male', 'Agender', 'Polygender', 'Male', 'Male', 'Polygender', 'Female', 'Male',
                          'Male', 'Non-binary', 'Polygender', 'Male', 'Non-binary', 'Male'])

    def test_filter(self):
        results = (Stream
                   .create(get_users())
                   .filter(lambda user: user['gender'] == 'Male')
                   .map(lambda user: user['gender'])
                   .asList())
        self.assertEqual(len(results), 12)

    def test_length(self):
        length = (Stream
                   .create(get_users())
                   .filter(lambda user: user['gender'] == 'Male')
                   .map(lambda user: user['gender'])
                   .length())
        self.assertEqual(length, 12)

    def test_reduce(self):
        sum_of_salaries = (Stream
                           .create(get_users())
                           .filter(lambda user: user['gender'] == 'Male')
                           .map(lambda user: user['salary'])
                           .reduce(operator.add)
                           )
        self.assertEqual(sum_of_salaries, 977023)

    def test_peek(self):
        peekCount = 0

        def increment_peek(data):
            nonlocal peekCount
            peekCount = peekCount + 1

        sum_of_salaries = (Stream
                           .create(get_users())
                           .filter(lambda user: user['gender'] == 'Male')
                           .map(lambda user: user['salary'])
                           .peek(increment_peek)
                           .reduce(operator.add)
                           )
        self.assertEqual(peekCount, 12)

    def test_skip(self):
        male_users_after_eighth = (Stream
                                     .create(get_users())
                                     .filter(lambda user: user['gender'] == 'Male')
                                     .skip(8)
                                     .asList()
                                     )
        self.assertEqual(male_users_after_eighth, [{'email': 'tlyburni@ca.gov',
                                                      'first_name': 'Timoteo',
                                                      'gender': 'Male',
                                                      'id': 19,
                                                      'ip_address': '92.149.164.27',
                                                      'last_name': 'Lyburn',
                                                      'salary': 121935},
                                                     {'email': 'ccoasterj@yandex.ru',
                                                      'first_name': 'Cly',
                                                      'gender': 'Male',
                                                      'id': 20,
                                                      'ip_address': '88.126.205.133',
                                                      'last_name': 'Coaster',
                                                      'salary': 85496},
                                                     {'email': 'scadoganm@aol.com',
                                                      'first_name': 'Syman',
                                                      'gender': 'Male',
                                                      'id': 23,
                                                      'ip_address': '19.248.170.11',
                                                      'last_name': 'Cadogan',
                                                      'salary': 54965},
                                                     {'email': 'wslowleyo@aol.com',
                                                      'first_name': 'Windham',
                                                      'gender': 'Male',
                                                      'id': 25,
                                                      'ip_address': '119.207.105.121',
                                                      'last_name': 'Slowley',
                                                      'salary': 94147}])

    def test_take(self):
        first_two_male_users = (Stream
                                    .create(get_users())
                                    .filter(lambda user: user['gender'] == 'Male')
                                    .take(2)
                                    .asList()
                                    )
        self.assertEqual(first_two_male_users, [{'email': 'jfranzini5@aol.com',
                                                     'first_name': 'Jasen',
                                                     'gender': 'Male',
                                                     'id': 6,
                                                     'ip_address': '169.28.108.16',
                                                     'last_name': 'Franzini',
                                                     'salary': 78373},
                                                    {'email': 'vsimester6@aol.com',
                                                     'first_name': 'Vasili',
                                                     'gender': 'Male',
                                                     'id': 7,
                                                     'ip_address': '233.8.45.246',
                                                     'last_name': 'Simester',
                                                     'salary': 78404}])
    def test_distinct(self):
        results = (Stream
                   .create(get_users())
                   .map(lambda user: user['gender'])
                   .distinct()
                   .asList())
        print("results", results)
        self.assertIsNotNone(results)
        self.assertIn('Male',results)
        self.assertIn('Female',results)
    def test_flat_map(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']


        product_stream= Stream.create(get_products())
        total_products = product_stream.length()
        products_of_rating_greater_than_three = (product_stream
                                            .stream()
                                        .filter(is_clothing)
                                        .peek(lambda data:print("peek is_clothing",data))
                                        .filter(is_rating_greater_than_three)
                                       )
        rating_values = (products_of_rating_greater_than_three
                                        .flatmap(reviews_from_product)
                                        .map(rating_from_review)
                                        .asList())

        product_prices_of_rating_greater_than_three = (products_of_rating_greater_than_three
                                        .stream()
                                        .map(price_from_product))

        product_prices = (product_prices_of_rating_greater_than_three
                                        .stream()
                                        .asList())
        product_prices_skipped_nine_items = (product_prices_of_rating_greater_than_three
                                        .stream()
                                        .skip(9)
                                        .asList())

        product_prices_skip_first_five_take_next_two_items = (product_prices_of_rating_greater_than_three
                                        .stream()
                                        .skip(5)
                                        .take(2)
                                        .asList())
        unique_product_prices = (product_prices_of_rating_greater_than_three
                                        .stream()
                                        .distinct()
                                        .asList())
        product_names = (products_of_rating_greater_than_three
                         .stream()
                         .map(name_from_product)
                         .asList())
        print("rating_values", rating_values)
        print("total_products", total_products)
        print("product_names", product_names)
        print("product_prices", product_prices)
        print("product_prices_skipped_nine_items", product_prices_skipped_nine_items)
        print("product_prices_skip_first_five_take_next_two_items", product_prices_skip_first_five_take_next_two_items)
        print("unique_product_prices", unique_product_prices)
        self.assertIsNotNone(rating_values)
        self.assertEqual(rating_values, [5, 1])
        self.assertEqual(product_prices, [1199.0, 1199.0, 999.0, 999.0, 899.0, 899.0, 1499.0, 5398.0, 2795.0, 2499.0])
        self.assertEqual(product_prices_skipped_nine_items, [ 2499.0])
        self.assertEqual(product_prices_skip_first_five_take_next_two_items, [ 899.0, 1499.0])
        self.assertEqual(unique_product_prices, [899.0, 2499.0, 999.0, 2795.0, 1199.0, 5398.0, 1499.0])
        self.assertEqual(total_products, 154)
        self.assertIn('Alisha Solid Women s Cycling Shorts',product_names)
        self.assertIn(5,rating_values)
        self.assertIn(1,rating_values)
