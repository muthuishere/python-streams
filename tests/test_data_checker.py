from shared.BaseUnitTest import BaseUnitTest
from streams.data_checker import isString


class TestDataChecker(BaseUnitTest):
    def test_isString_accepts_empty_and_unicode_but_rejects_bytes(self):
        self.assertTrue(isString(''))
        self.assertTrue(isString('héllo'))
        self.assertFalse(isString(b'x'))
        self.assertFalse(isString(1))
        self.assertFalse(isString(None))
        self.assertFalse(isString(['a']))
