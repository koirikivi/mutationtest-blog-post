from unittest import TestCase
from testprogram import bigger_number

class BiggerNumberTests(TestCase):
    def test_2_is_bigger_than_1(self):
        assert bigger_number(2, 1) == 2

    def test_1_is_smaller_than_2(self):
        assert bigger_number(1, 2) == 2
