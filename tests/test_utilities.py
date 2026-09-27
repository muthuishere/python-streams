from shared.BaseUnitTest import BaseUnitTest
from streams.utilities import chunk


class TestUtilities(BaseUnitTest):
    def test_chunk_splits_into_tuples_and_zero_drops_every_element(self):
        self.assertEqual([(0, 1, 2), (3, 4, 5), (6,)], list(chunk(3, range(7))))
        self.assertEqual([1000, 1000, 500],
                         [len(current_chunk) for current_chunk in chunk(1000, range(2500))])
        self.assertEqual([], list(chunk(3, [])))
        self.assertEqual([(1, 2, 3)], list(chunk(None, [1, 2, 3])))
        self.assertEqual([], list(chunk(0, [1, 2, 3])))

        chunks = chunk(3, range(7))
        self.assertEqual((0, 1, 2), next(chunks))
        self.assertEqual((3, 4, 5), next(chunks))
        self.assertEqual((6,), next(chunks))

        one_shot_chunks = chunk(2, [1, 2, 3])
        self.assertEqual([(1, 2), (3,)], list(one_shot_chunks))
        self.assertEqual([], list(one_shot_chunks))

        for invalid_number in (-1, 2.5):
            with self.assertRaises(ValueError) as context:
                list(chunk(invalid_number, [1, 2, 3]))
            self.assertIn('Stop argument for islice()', str(context.exception))

        with self.assertRaises(TypeError):
            list(chunk(2, 5))
