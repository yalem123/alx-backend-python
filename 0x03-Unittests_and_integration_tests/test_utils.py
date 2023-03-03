#!/usr/bin/env python3
"""
Module test_utils
"""
from parameterized import parameterized
import unittest
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for test_access_nested_map()
    """
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access nested map with key path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"])
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test a KeyError is raised
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test case for get_json()"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, url, payload):
        """Should return expected result"""
        with patch('utils.get_json', return_value=payload) as mock:
            res = mock(url)
            mock.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """
    Test case for memoize
    """
    def test_memoize(self):
        """Test calls for memoize"""

        class TestClass:
            """nested test class"""

            def a_method(self):
                """ a_method() """
                return 42

            @memoize
            def a_property(self):
                """a_property method"""
                return self.a_method

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()

            test_class.a_property
            test_class.a_property

            mock_method.assert_called_once

