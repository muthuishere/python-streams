from unittest import TestCase

from shared.FileUtilities import file_exists, get_file_contents


class BaseUnitTest(TestCase):
    def assertListContains(self, fullList, containsList):
        for item in containsList:
            self.assertIn(item,fullList)
    def assertListEqualsInAnyOrder(self, fullList, containsList):
            self.assertEqual(sorted(fullList) , sorted(containsList))

    def assertFileExists(self, filename):
            self.assertTrue(file_exists(filename))

    def assertFileContents(self, filename,contents):
            actual_contents = get_file_contents(filename)
            self.assertEqual(actual_contents, contents)

    def assertFileContentContains(self, filename,contents):
            actual_contents = get_file_contents(filename)
            self.assertIn(contents, actual_contents)
