#!/usr/bin/env python3
# """ The project module contains the first unit test
# for utils.access_nested_map.
# """

# import unittest
# from unittest.mock import patch
# from utils import access_nested_map, get_json, memoize
# from parameterized import parameterized


# class TestAccessNestedMap(unittest.TestCase):
#     """ TestAccessNestedMap inherits from unittest. TestCase to test
#     utils.access_nested_map.
#     """
#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2)
#     ])
#     def test_access_nested_map(self, nested_map, path, expected_result):
#         """ Tests if access_nested_map method returns what it is supposed to.
#         """
#         self.assertEqual(access_nested_map(nested_map, path), expected_result)

#     @parameterized.expand([
#         ({}, ("a",)),
#         ({"a": 1}, ("a", "b"))
#     ])
#     def test_access_nested_map_exception(self, nested_map, path):
#         """ Tests if access_nested_map method raise an exception.
#         """
#         self.assertRaises(KeyError, access_nested_map, nested_map, path)


# class TestGetJson(unittest.TestCase):
#     """ TestAccessNestedMap inherits from unittest. TestCase to test
#     utils.get_json.
#     """
#     @parameterized.expand([
#         ("http://example.com", {"payload": True}),
#         ("http://holberton.io", {"payload": False})
#     ])
#     def test_get_json(self, test_url, test_payload):
#         """ Tests if get_json method returns the expected result.
#         """
#         with patch('requests.get') as mock:
#             mock.return_value.json.return_value = test_payload
#             self.assertEqual(get_json(test_url), test_payload)
#             mock.assert_called_once()


# class TestMemoize(unittest.TestCase):
#     """ TestMemoize inherits from unittest. TestCase to test
#     utils.memoize.
#     """

#     def test_memoize(self):
#         """Tests if memoize returns the correct result after a_property
#         is called twice.
#         """
#         class TestClass:
#             """ TestClass to test utils.memoize."""

#             def a_method(self):
#                 """Method that returns 42"""
#                 return 42

#             @memoize
#             def a_property(self):
#                 """Method that returns a_method"""
#                 return self.a_method()

#         with patch.object(TestClass, 'a_method', return_value=42) as mock:
#             tc = TestClass()
#             self.assertEqual(tc.a_property, mock.return_value)
#             self.assertEqual(tc.a_property, mock.return_value)
#             mock.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()


"""
Test suite for the utils module.
This file contains unit tests for the functions in utils.py.
"""
import unittest
import requests
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests that access_nested_map returns the expected value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Tests that a KeyError is raised for invalid paths and the message is correct.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Test suite for the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Tests that get_json returns the expected payload.
        """
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)



if __name__ == '__main__':
    unittest.main()
