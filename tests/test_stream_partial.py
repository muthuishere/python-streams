from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.CustomProfiler import start_profiler, stop_profiler
from shared.users import get_users

import cProfile
import pstats

from streams.Stream import Stream
from shared.users import get_200_users


class TestStreamPartials(BaseUnitTest):
    def test_product_names_from_partial_streams(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()

        start_profiler()
        product_stream = Stream.create(products)
        product_names = (product_stream
                        .stream()
                         .map(name_from_product)
                         .asList())
        product_prices = (product_stream
                            .stream()
                          .map(price_from_product)
                          .asList())
        stop_profiler()

        print(product_names)
        self.assertListEqualsInAnyOrder(
            ['Alisha Solid Women s Cycling Shorts', 'FabHomeDecor Fabric Double Sofa Bed', 'AW Bellies',
             'Alisha Solid Women s Cycling Shorts', 'Sicons All Purpose Arnica Dog Shampoo',
             'Alisha Solid Women s Cycling Shorts', 'FabHomeDecor Fabric Double Sofa Bed',
             'dilli bazaaar Bellies  Corporate Casuals  Casuals', 'Alisha Solid Women s Cycling Shorts',
             'Ladela Bellies', 'Carrel Printed Women s', 'Alisha Solid Women s Cycling Shorts',
             'Freelance Vacuum Bottles 350 ml Bottle', 'Alisha Solid Women s Cycling Shorts',
             'FabHomeDecor Fabric Double Sofa Bed', 'Style Foot Bellies', 'Carrel Printed Women s',
             'FabHomeDecor Fabric Double Sofa Bed', 'Sicons Conditioning Conditoner Dog Shampoo',
             'dongli Printed Boy s Round Neck T-Shirt', 'SWAGGA Women Clogs',
             'Kennel Rubber Dumbell With Bell - Small Rubber Rubber Toy For Dog', 'Glus Wedding Lingerie Set',
             'Veelys Shiny White Quad Roller Skates - Size 4.5 UK', 'Bulaky vanity case Jewellery Vanity Case',
             'FDT Women s Leggings', 'Madcaps C38GR30 Men s Cargos',
             'Indcrown Net Embroidered Semi-stitched Lehenga Choli Material',
             'Shopmania Music Band A5 Notebook Spiral Bound', 'Shopmania Music Band A5 Notebook Spiral Bound',
             'Tiara Diaries 2016-2017 Designer LA Kaarta #TAKING ACTION GETTING RESULT# (Set of 3) B5 Notebook Hard Bound',
             'KAJCI Embroidered Women s Waistcoat',
             'Packman 8 x 10 inches Security Bags Without POD Jacket Courier Bag Security Bag',
             'Pick Pocket Embroidered Women s Waistcoat', 'Angelfish Silk Potali Potli', 'Oye Boy s Dungaree',
             'Nuride Canvas Shoes', 'OM SHIVAKRITI Square wall Clock Showpiece  -  38.1 cm',
             'Himmlisch ST381 Magnetic Sun Shade For Maruti Alto', 'Rapter BNC-179 BNC Wire Connector',
             'Rapter BNC-047 BNC Wire Connector', 'Roadster Men s Zipper Solid Cardigan', 'HRS ULTIMATE BOY Chest Pads',
             'Vermello Men Casual Brown Genuine Leather Belt', 'HRS CLUB BOY Thigh Pads',
             'Ligans NY Men Formal Black Genuine Leather Belt',
             'Elegance Polyester Multicolor Abstract Eyelet Door Curtain', 'Liza Women Wedges',
             'HRS ULTIMATE BOY Elbow Pads', 'Sathiyas Cotton Bath Towel', 'HRS ULTIMATE MEN Chest Pads',
             'SANTOSH ROYAL FASHION Cotton Printed King sized Double Bedsheet',
             'CASEDEAL Microsoft Nokia lumia x2 Back Panel', 'Mario Gotze Women s Printed Casual Orange Shirt',
             'Jaipur Print Cotton Floral King sized Double Bedsheet', 'Shilpi NHSCN003 Coin Bank',
             'Jaipur Print Cotton Floral King sized Double Bedsheet', 'Babeezworld Dungaree Baby Boy s  Combo',
             'Redbag Eight Armed Goddess Sherawali Maa Showpiece  -  10.8 cm', 'Proence Weight Gainers  Mass Gainers',
             'Discountgod Men s Checkered Casual Shirt', 'Silver Streak Men s Printed Casual Denim Shirt',
             'Cobra Paris CO6394A1 Analog Watch  - For Men  Boys',
             'Aries Gold G 729 S-BK Analog Watch  - For Men  Boys', 'Carlton Boots',
             'Maserati Time R8851116001 Analog Watch  - For Boys',
             'Camerii WM64 Elegance Analog Watch  - For Men  Boys', 'Reckler Slim Fit Men s Jeans',
             'Quechua Arpenaz Novadry Boots', 'Colat COLAT_MW20 Sheen Analog Watch  - For Men  Women  Boys  Girls',
             'Steppings Trendy Boots', 'Rochees RW38 Analog Watch  - For Boys', 'Catwalk Boots',
             'Magnum Footwear Lifestyle', 'Rialto Boots', 'Kielz Ladies Boots',
             'Alfajr WY16B Youth Digital Watch  - For Men  Boys', 'La Briza Ashley Boots',
             'TAG Heuer CAU1116.BA0858 Formula 1 Analog Watch  - For Boys  Men', 'Shuz Touch Boots',
             'Wrangler Skanders Fit Men s Jeans', 'Costa Swiss CS-2001 Analog Watch  - For Boys  Men', 'Crocs Boots',
             'Lyc White Casual Boots', 'Myra Comfortable Boots', 'Get Glamr Designer Uggy Boots', 'Kielz Ladies Boots',
             'Kielz Ladies Boots', 'Rochees RW50 Analog Watch  - For Boys', 'Kielz Ladies Boots',
             'Salt N Pepper 13-516 Greta Red Boots', 'Fluid DMF-002-GR01 Digital Watch  - For Boys', 'Rialto Boots',
             'Steppings Trendy Boots', 'Disney DW100230 Digital Watch  - For Boys  Girls',
             'Salt N Pepper 13-167 Marsha Red Boots', 'Cartier W6701005 Analog Watch  - For Boys  Men',
             'Bruno Manetti Cannelita Boots', 'Stylistry Maxis Shde6603brwoboot3104 Boots',
             'Lois Caron LCS-4032 Analog Watch  - For Boys  Men', 'Felix Y 39 Analog Watch  - For Boys  Men',
             'Kielz Boots', 'Kielz Ladies Boots', 'Sakay Country Leather Boots',
             'Kool Kidz DMK-012-QU02 Analog Watch  - For Girls  Boys',
             'Franck Bella FB0128B Analog Watch  - For Men  Boys', 'Steppings Trendy Boots',
             'Kool Kidz DMK-003-YL 03 Analog Watch  - For Girls  Boys',
             'Casela CAS-W-13 Basic Analog Watch  - For Boys  Girls', 'Sneha Unique Boots',
             'Timer TC_-_690143 Analog Watch  - For Boys', 'NE Regular Fit Men s Jeans', 'Shuz Touch Boots',
             'Kielz Ladies Boots', 'Colat COLAT_M08 Roman Numerals Analog Watch  - For Men  Boys', 'Kielz Ladies Boots',
             'Belle Gambe Boots', 'Titan 1639SL03 Analog Watch  - For Boys  Men', 'Clincher Semonday Boots',
             'Srushti Art Jewelry Megnet_Led_Sport_BlackRed1 Digital Watch  - For Men  Women  Boys  Girls',
             'Kielz Ladies Boots', 'Q&Q VQ13-008 Analog Watch  - For Girls  Boys', 'Belle Gambe Boots', 'Roxy Boots',
             'Lee Men s Jeans', 'Bruno Manetti 676 Boots', 'Estilo 1056 Analog Watch  - For Boys  Men',
             'Jack klein BlackLed Digital Watch  - For Boys',
             'North Moon IW-005-FK Silicone Ion Digital Watch  - For Boys  Girls  Women', 'Shuz Touch Boots',
             'Foot Candy Boots', 'Credos Boots', 'Rich Club Apple Shaped LED Digital Watch  - For Boys  Girls',
             'Skmei AD1031-Black Formal Analog-Digital Watch  - For Men  Boys', 'Kielz Ladies Boots',
             'Kms Ironman_Look_Led_Black11 Digital Watch  - For Men  Women  Girls  Boys', 'Anand Archies Boots',
             'Steppings Trendy Boots', 'Swag 670038 Analog Watch  - For Boys', 'Roadster Skinny Fit Fit Men s Jeans',
             'Selfie Black Denim Boots', 'Q&Q LLA2-213 Digital Watch  - For Boys  Girls', 'Belle Gambe Winter Boots',
             'Hala Red In Black trendy digital Digital Watch  - For Boys  Girls  Men', 'Kielz Ladies Boots',
             'Kielz Boots', 'Franck Bella FB74C Analog Watch  - For Boys  Men', 'Carlton London Boots',
             'Ridas Apl_led_black Apple Shape Digital Watch  - For Boys', 'Shuz Touch Boots', 'La Briza Andria Boots',
             'Skmei 1070BLK Sports Analog-Digital Watch  - For Men  Boys', 'Kielz Ladies Boots',
             'Carlton London Boots'], product_names)
        self.assertListEqualsInAnyOrder(
            [999.0, 32157.0, 999.0, 699.0, 220.0, 1199.0, 32157.0, 699.0, 1199.0, 1724.0, 2299.0, 999.0, 699.0, 999.0,
             32157.0, 899.0, 2499.0, 32157.0, 110.0, 2400.0, 1500.0, 190.0, 1299.0, 3199.0, 499.0, 699.0, 2199.0, 999.0,
             499.0, 499.0, 1000.0, 1200.0, 350.0, 899.0, 999.0, 899.0, 1999.0, 1499.0, 6999.0, 2299.0, 1299.0, 1399.0,
             440.0, 1495.0, 280.0, 795.0, 1899.0, 1990.0, 250.0, 600.0, 440.0, 2699.0, 1999.0, 1499.0, 2599.0, 900.0,
             2599.0, 999.0, 1600.0, 1025.0, 750.0, 1299.0, 18995.0, 13699.0, 3495.0, 24400.0, 1099.0, 5398.0, 2499.0,
             3999.0, 1799.0, 1415.0, 2095.0, 3999.0, 3295.0, 2499.0, 5495.0, 2299.0, 107750.0, 1499.0, 2795.0, 1199.0,
             3995.0, 1199.0, 1049.0, 3499.0, 2299.0, 1999.0, 1120.0, 2799.0, 3495.0, 1699.0, 3295.0, 3499.0, 350.0,
             3695.0, 201000.0, 3399.0, 2199.0, 1200.0, 1550.0, 2999.0, 2299.0, 3999.0, 375.0, 1199.0, 2199.0, 475.0,
             3999.0, 1799.0, 1299.0, 4999.0, 2995.0, 2499.0, 4999.0, 2299.0, 3999.0, 1795.0, 3499.0, 799.0, 2499.0,
             585.0, 3499.0, 19995.0, 2699.0, 2999.0, 1299.0, 999.0, 235.0, 1499.0, 2899.0, 4499.0, 999.0, 2499.0,
             2799.0, 1395.0, 499.0, 2199.0, 2499.0, 2499.0, 1000.0, 645.0, 3499.0, 399.0, 2499.0, 2499.0, 1299.0,
             2295.0, 349.0, 4495.0, 2099.0, 2345.0, 1899.0, 1995.0], product_prices)



