from pyspark.sql import SparkSession
import unittest


class TestMain(unittest.TestCase):
    def add(self, a, b):
        return a + b

    def test_addition(self):
        result = self.add(3, 5)
        assert result == 8

    def test_negative_numbers(self):
        result = self.add(-2, 2)
        assert result == 0


if __name__ == "__main__":
    unittest.main()
