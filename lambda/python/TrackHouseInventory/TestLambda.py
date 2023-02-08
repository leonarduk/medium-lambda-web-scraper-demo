import unittest

import lambda_function as l


class MyTestCase(unittest.TestCase):
    def test_something(self):
        value = l.fetchField("Total unique homes for sale found:", "https://www.home.co.uk/company/stats.htm")


if __name__ == '__main__':
    unittest.main()
