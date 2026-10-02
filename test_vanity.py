import math
import unittest

from vanity import difficulty, keys_for


class VanityTest(unittest.TestCase):
    def test_evm(self):
        self.assertEqual(difficulty("0xdead"), ("evm", 16 ** 4))
        self.assertEqual(difficulty("0xDeAd", case_sensitive=True), ("evm", 16 ** 4 * 2 ** 4))
        self.assertEqual(difficulty("0x1234", case_sensitive=True)[1], 16 ** 4)

    def test_base58(self):
        self.assertEqual(difficulty("sol:Moon"), ("sol", 58 ** 4))
        self.assertEqual(difficulty("btc:1Kid"), ("btc", 58 ** 3))

    def test_invalid(self):
        for bad in ("0xzz", "sol:0OIl", "btc:3abc", "eth:abc"):
            with self.assertRaises(ValueError):
                difficulty(bad)

    def test_median_is_about_ln2_times_d(self):
        d = 16 ** 6
        self.assertAlmostEqual(keys_for(0.5, d) / d, math.log(2), places=4)


if __name__ == "__main__":
    unittest.main()
