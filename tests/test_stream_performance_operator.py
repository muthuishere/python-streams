from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.CustomProfiler import start_profiler, stop_profiler

from streams.Stream import Stream
from shared.users import get_200_users
from streams.operations.operators import item


class TestStreamPerformanceOperator(BaseUnitTest):
    def test_compose_functions_functional_stream_long_method(self):
        products = get_products()

        start_profiler()

        # 383 function calls in 0.001 seconds
        # Total allocated size: 13.8 KiB
        product_stream = Stream.create(products)
        total_products_with_rating_greater_than_3 = (product_stream
                                                     .stream()
                                                     .filter(item['overAllRating'] > 3)
                                                     .length())
        prices_for_clothes = (product_stream
                              .stream()
                              .filter(item['category'] == 'Clothing')
                              .map(item['price'])
                              .distinct()
                              .skip(5)
                              .take(8)
                              .asList()
                              )

        stop_profiler()
        print(total_products_with_rating_greater_than_3)
        print(prices_for_clothes)
        self.assertEqual(57, total_products_with_rating_greater_than_3)
        self.assertListEqualsInAnyOrder([2795.0, 2699.0, 750.0, 1199.0, 2299.0, 1200.0, 1299.0, 1499.0],
                                        prices_for_clothes)

    def test_compose_functions_functional_stream_another_long_method(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        price_from_product = lambda product: product['price']

        products = get_products()

        start_profiler()

        # 392 function calls in 0.000 seconds
        product_stream = Stream.create(products)
        total_products_with_rating_greater_than_3 = (product_stream
                                                     .stream()
                                                     .filter(is_rating_greater_than_three)
                                                     .length())
        prices_for_clothes = (product_stream
                              .stream()
                              .filter(is_clothing)
                              .map(price_from_product)
                              .asSet()
                              )

        stop_profiler()
        print(total_products_with_rating_greater_than_3)
        print(prices_for_clothes)
        self.assertEqual(57, total_products_with_rating_greater_than_3)
        self.assertListEqualsInAnyOrder([2400.0, 2499.0, 899.0, 999.0, 4999.0, 2795.0, 2699.0, 750.0, 1199.0, 2299.0, 1200.0, 1299.0, 1499.0, 2199.0, 5398.0, 699.0, 1399.0],
                                        prices_for_clothes)

    def test_compose_functions_users_functional_stream(self):

        users = get_200_users()
        start_profiler()

        # 510 function calls in 0.000 seconds
        #Total allocated size: 6.7 KiB
        results = (Stream.create(users)
                   .filter(item['salary'] > 50000)
                   .filter(item['gender'] == "Male")
                   .map(item['first_name'])
                   .asList()
                   )

        stop_profiler()

        print("results", results)

        self.assertListContains(
            ['Jasen', 'Vasili', 'Lind', 'Darbee', 'Britte', 'Layton', 'Rosabelle', 'Wiley', 'Timoteo', 'Cly', 'Syman',
             'Windham'], results)


