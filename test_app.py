import unittest
import sys
from unittest import mock
from app import app


class TestClientMethods(unittest.TestCase):

    def test_start_page(self):
        response = app.test_client().get('/help')
        print(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
