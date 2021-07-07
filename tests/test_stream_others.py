from unittest import TestCase

from shared.products import get_products
from shared.users import get_users

import cProfile
import pstats

from streams.Stream import Stream


def profile_method(fn):
    profiler = cProfile.Profile()
    profiler.enable()
    data = fn()
    profiler.disable()
    pstats.Stats(profiler).print_stats()
    return data
users = [
            {
                "id": 1,
                "first_name": "Mandy",
                "last_name": "Gowan",
                "email": "mgowan0@aol.com",
                "gender": "Female",
                "loves": ['Soccer', 'Cricket', 'Golf'],
                "salary": 119885
            },
            {
                "id": 2,
                "first_name": "Janessa",
                "last_name": "Cotterell",
                "email": "jcotterell1@aol.com",
                "gender": "Female",
                "loves": ['Cricket'],
                "salary": 107629
            },
            {
                "id": 6,
                "first_name": "Jasen",
                "last_name": "Franzini",
                "email": "jfranzini5@aol.com",
                "gender": "Male",
                "loves": ['Soccer', 'Golf'],
                "salary": 78373
            }
        ]


class TestStream(TestCase):
    def test_example_1(self):
        results = (Stream
                   .create(users)
                   .filter(lambda user:user['salary'] > 80000)
                   .map(lambda user: user['first_name'])
                   .asList())
        #['Mandy', 'Janessa']
        print(results)
    def test_example_2(self):
        results = (Stream
                   .create(users)
                   .flatmap(lambda user:user['loves'] )
                   .distinct()
                   .asList())
        #['Cricket', 'Golf', 'Soccer']
        print(results)
    def test_example_3(self):
        results = (Stream
                   .create(users)
                   .skip(1)
                   .take(1)
                   .map(lambda user: user['first_name'])
                   .asList())

        #['Janessa']
        self.assertEqual(results, ['Janessa'])
        print(results)
    def test_flatmap(self):
        results = (Stream
                   .create(users)
                   .flatmap(lambda user:user['loves'] )
                   .asList())
        print(results)
        self.assertEqual(results,['Soccer', 'Cricket', 'Golf', 'Cricket', 'Soccer', 'Golf'])
        #['Soccer', 'Cricket', 'Golf', 'Cricket', 'Soccer', 'Golf']
    def test_fromList_with_map(self):
        # filter(lambda user: user['gender'] == gender, users)

        results = Stream.create(get_users()).map(lambda user: user['gender']).asList()
        print("results", results)
        self.assertIsNotNone(results)
        self.assertEqual(results,
                         ['Female', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Male',
                          'Female', 'Male', 'Agender', 'Polygender', 'Male', 'Male', 'Polygender', 'Female', 'Male',
                          'Male', 'Non-binary', 'Polygender', 'Male', 'Non-binary', 'Male'])

    def test_fromList_with_map_filter(self):
        # filter(lambda user: user['gender'] == gender, users)

        results = Stream.create(get_users()).map(lambda user: user['gender']).filter(
            lambda g: g == 'Agender').asList()
        print("results", results)
        self.assertIsNotNone(results)
        self.assertEqual(results, ['Agender'])

    def test_fromList_with_map_filter_with_profile(self):
        current_method = lambda: Stream.create(get_users()).map(lambda user: user['gender']).filter(
            lambda g: g == 'Female').asList()
        results = profile_method(current_method)
        print("results", results)
        self.assertIsNotNone(results)
        self.assertEqual(results, ['Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female'])

    def test_fromList_with_map_filter_with_clothing_overallrating(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        name_from_product = lambda product: product['name']

        current_method = lambda: (Stream.create(get_products())
                                        .filter(is_clothing)
                                        .filter(is_rating_greater_than_three)
                                        .map(name_from_product)
                                        .asList())

        results = profile_method(current_method)
        print("results", results)
        self.assertIsNotNone(results)
        self.assertEqual(results, ['Alisha Solid Women s Cycling Shorts',
                                   'Alisha Solid Women s Cycling Shorts',
                                   'Alisha Solid Women s Cycling Shorts',
                                   'Alisha Solid Women s Cycling Shorts',
                                   'Indcrown Net Embroidered Semi-stitched Lehenga Choli Material',
                                   'Pick Pocket Embroidered Women s Waistcoat',
                                   'Oye Boy s Dungaree',
                                   'Mario Gotze Women s Printed Casual Orange Shirt',
                                   'Reckler Slim Fit Men s Jeans',
                                   'Wrangler Skanders Fit Men s Jeans',
                                   'Roadster Skinny Fit Fit Men s Jeans'])

    def test_fromList_with_map_filter_with_clothing_overallrating_get_reviews(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']


        current_method = lambda: (Stream
                                        .create(get_products())
                                        .filter(is_clothing)
                                        .filter(is_rating_greater_than_three)
                                        .flatmap(reviews_from_product)
                                        .map(rating_from_review)
                                        .asList())

        results = profile_method(current_method)
        print("results", results)
        self.assertIsNotNone(results)
        self.assertEqual(results, [5, 1, 2, 2, 1, 3, 2, 1, 2, 5, 1, 4, 1, 5, 5, 1])
        self.assertIn(5,results)
        self.assertIn(1,results)

    def test_fromList_with_map_filter_with_clothing_overallrating_inter(self):

            def current_method():
                return list(map(lambda product: product['name'],  filter(lambda product: product['overAllRating'] > 3, filter(lambda product: product['category'] == 'Clothing',get_products()))))


            results = profile_method(current_method)
            print("results", results)
            self.assertIsNotNone(results)
            self.assertEqual(results, ['Alisha Solid Women s Cycling Shorts',
                                       'Alisha Solid Women s Cycling Shorts',
                                       'Alisha Solid Women s Cycling Shorts',
                                       'Alisha Solid Women s Cycling Shorts',
                                       'Indcrown Net Embroidered Semi-stitched Lehenga Choli Material',
                                       'Pick Pocket Embroidered Women s Waistcoat',
                                       'Oye Boy s Dungaree',
                                       'Mario Gotze Women s Printed Casual Orange Shirt',
                                       'Reckler Slim Fit Men s Jeans',
                                       'Wrangler Skanders Fit Men s Jeans',
                                       'Roadster Skinny Fit Fit Men s Jeans'])

