from unittest import TestCase


class BaseUnitTest(TestCase):
    def assertListContains(self, fullList, containsList):
        for item in containsList:
            self.assertIn(item,fullList)
